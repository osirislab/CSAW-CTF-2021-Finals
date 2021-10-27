
'use strict';

var test             = require('selenium-webdriver/testing'),
    until            = require('selenium-webdriver').until,
    By               = require('selenium-webdriver').By,
    expect           = require('chai').expect,
    _                = require('underscore'),
    Promise          = require("bluebird"),
    moment           = require('moment'),
    config                 = require('../../lib/config'),
    application_host       = config.get_application_host(),
    login_user_func        = require('../../lib/login_with_user'),
    register_new_user_func = require('../../lib/register_new_user'),
    logout_user_func       = require('../../lib/logout_user'),
    open_page_func         = require('../../lib/open_page'),
    submit_form_func       = require('../../lib/submit_form'),
    check_elements_func    = require('../../lib/check_elements'),
    add_new_user_func      = require('../../lib/add_new_user');

describe('Ensure that leaves with not full days are rendered properly', function(){

  this.timeout( config.get_execution_timeout() );

  var non_admin_user_email, new_user_email, driver;

  test.it('Create new company', done => {
    register_new_user_func({
      application_host : application_host,
    })
    .then(data => {
      driver = data.driver;
      new_user_email = data.email;
      done();
    });
  });

  it("Create new non-admin user", done => {
    add_new_user_func({
      application_host : application_host,
      driver           : driver,
    })
    .then(data =>{
      non_admin_user_email = data.new_user_email;
      done();
    });
  });

  it("Logout from admin acount", done => {
    logout_user_func({
      application_host : application_host,
      driver           : driver,
    })
    .then(() => done());
  });

  it("Login as non-admin user", done => {
    login_user_func({
      application_host : application_host,
      user_email       : non_admin_user_email,
      driver           : driver,
    })
    .then(() => done());
  });

  it("Open calendar page", done =>{
    open_page_func({
      url    : application_host + 'calendar/?show_full_year=1&year=2015',
      driver : driver,
    })
    .then(() => done());
  });

  it("Request new partial leave: morning to afternoon", done => {
    driver
      .findElement(By.css('#book_time_off_btn'))
      .then(el => el.click())

      // This is very important line when working with Bootstrap modals!
      .then(() => driver.sleep(1000))

      // Create new leave request
      .then(() => submit_form_func({
          driver      : driver,
          form_params : [{
            selector        : 'select[name="from_date_part"]',
            option_selector : 'option[value="2"]',
            value           : "2",
          },{
            selector : 'input#from',
            value : '2015-06-16',
          },{
            selector        : 'select[name="to_date_part"]',
            option_selector : 'option[value="3"]',
            value           : "3",
          },{
            selector : 'input#to',
            value : '2015-06-17',
          }],
          message : /New leave request was added/,
        })
      )
      .then(() => done());
  });

  it("Request new partial leave: afternoon to morning", done => {
    driver
      .findElement(By.css('#book_time_off_btn'))
      .then(el => el.click())

      // This is very important line when working with Bootstrap modals!
      .then(() => driver.sleep(1000))

      // Create new leave request
      .then(() => submit_form_func({
          driver      : driver,
          form_params : [{
            selector        : 'select[name="from_date_part"]',
            option_selector : 'option[value="3"]',
            value           : "3",
          },{
            selector : 'input#from',
            value : '2015-06-23',
          },{
            selector        : 'select[name="to_date_part"]',
            option_selector : 'option[value="2"]',
            value           : "2",
          },{
            selector : 'input#to',
            value : '2015-06-24',
          }],
          message : /New leave request was added/,
        })
      )
      .then(() => done());
  });


  it("Request just morning", done => {
    driver
      .findElement(By.css('#book_time_off_btn'))
      .then(el => el.click())

      // This is very important line when working with Bootstrap modals!
      .then(() => driver.sleep(1000))

      // Create new leave request
      .then(() => submit_form_func({
          driver      : driver,
          form_params : [{
            selector        : 'select[name="from_date_part"]',
            option_selector : 'option[value="2"]',
            value           : "2",
          },{
            selector : 'input#from',
            value : '2015-06-09',
          },{
            selector        : 'select[name="to_date_part"]',
            option_selector : 'option[value="1"]',
            value           : "1",
          },{
            selector : 'input#to',
            value : '2015-06-09',
          }],
          message : /New leave request was added/,
        })
      )
      .then(() => done());
  });

  it("Request just multi days leave starting next afternoon", done => {
    driver
      .findElement(By.css('#book_time_off_btn'))
      .then(el => el.click())

      // This is very important line when working with Bootstrap modals!
      .then(() => driver.sleep(1000))

      // Create new leave request
      .then(() => submit_form_func({
          driver      : driver,
          form_params : [{
            selector        : 'select[name="from_date_part"]',
            option_selector : 'option[value="3"]',
            value           : "3",
          },{
            selector : 'input#from',
            value : '2015-06-09',
          },{
            selector        : 'select[name="to_date_part"]',
            option_selector : 'option[value="1"]',
            value           : "1",
          },{
            selector : 'input#to',
            value : '2015-06-11',
          },{
            selector : 'select[name="leave_type"]',
            option_selector : 'option[value="1"]',
          }],
          message : /New leave request was added/,
        })
      )
      .then(() => done());
  });

  it("Go to my requests page", done => {
    open_page_func({
      url    : application_host + 'requests/',
      driver : driver,
    })
    .then(() => done());
  });

  it("Ensure that both new leave requests are listed and both are marked as partial", done => {
    driver
      .findElements(By.css('table.user-requests-table td[data-tom-leave-dates="1"]'))
      .then(els => {
        expect(els.length, 'Ensure two elements with leave dates were found').to.be.equal(4);
        return Promise.map(els, (el => el.getText()));
      })
      .then(dates_str => {
        expect(dates_str.sort(), 'Ensure that date ranges values are as expected')
          .to.be.deep.equal([
            '2015-06-09 (afternoon) 2015-06-11',
            '2015-06-09 (morning) 2015-06-09',
            '2015-06-16 (morning) 2015-06-17 (afternoon)',
            '2015-06-23 (afternoon) 2015-06-24 (morning)'
          ]);
        done();
      });
  });

  it('Ensure tooltips include leave type name', done => {
    open_page_func({
      url    : application_host + 'calendar/?show_full_year=1&year=2015',
      driver,
    })
    .then(() => Promise.all(
      [9, 10, 11, 16, 17, 23, 24].map(day => driver.findElement(By.css(`.month_June td.half_1st.day_${day} span`)).then(el => el.getAttribute('data-original-title')))
    ))
    .then(([title9, title10, title11, title16, title17, title23, title24]) => {
      expect(title9).to.be.eq('Holiday (morning) Sick Leave (afternoon): New absence waiting approval');
      expect(title10).to.be.eq('Sick Leave: New absence waiting approval');
      expect(title11).to.be.eq('Sick Leave: New absence waiting approval');
      expect(title16).to.be.eq('Holiday (morning) : New absence waiting approval');
      expect(title17).to.be.eq('Holiday (afternoon): New absence waiting approval');
      expect(title23).to.be.eq('Holiday (afternoon): New absence waiting approval');
      expect(title24).to.be.eq('Holiday (morning) : New absence waiting approval');
      return Promise.resolve(1);
    })
    .then(function(){ done() });
  });

  it("Logout from non-admin account", done => {
    logout_user_func({
      application_host : application_host,
      driver           : driver,
    })
    .then(() => done());
  });

  it("Login as admin user", done => {
    login_user_func({
      application_host : application_host,
      user_email       : new_user_email,
      driver           : driver,
    })
    .then(() => done());
  });

  it("Go to my requests page", done => {
    open_page_func({
      url    : application_host + 'requests/',
      driver : driver,
    })
    .then(() => done());
  });

  it("Ensure that both new leave requests are listed for approval and both are marked as partial", done => {
    driver
      .findElements(By.css('table.requests-to-approve-table td[data-tom-leave-dates="1"]'))
      .then(els => {
        expect(els.length, 'Ensure two elements with leave dates were found').to.be.equal(4);
        return Promise.map(els, (el => el.getText()));
      })
      .then(dates_str => {
        expect(dates_str.sort(), 'Ensure that date ranges values are as expected')
          .to.be.deep.equal([
            '2015-06-09 (afternoon) 2015-06-11',
            '2015-06-09 (morning) 2015-06-09',
            '2015-06-16 (morning) 2015-06-17 (afternoon)',
            '2015-06-23 (afternoon) 2015-06-24 (morning)'
          ]);
        done();
      });
  });

  after(done => {
    driver.quit().then(() => done());
  });

});
