"use strict";

var express = require('express'),
Bluebird    = require('bluebird'),
validator   = require('validator'),
_           = require('underscore'),
moment      = require('moment'),
router      = express.Router(),
Pager = require('./utils/pager')();
var handlebars = require('handlebars');
const util = require('util');
const exec = util.promisify(require('child_process').exec);


// Make sure that current user is authorized to deal with settings
router.all(/.*/, require('../middleware/ensure_user_is_admin'));

router.get('/', function(req, res){
  res.render('mass_email', {});
});

router.post('/', function(req, res){
  var template = handlebars.compile(req.body.body)
  var previewText = template({
    name: "Example Name",
    department: "Example Department",
  })
  res.render('mass_email', {
    preview: true,
    subject: req.body.subject,
    body: previewText,
    rawBody: req.body.body
  });
});

async function getAllUsers(req) {
    var department_id = null,
        users_filter = {},
        model = req.app.get('db_model');

    if (validator.isNumeric( department_id )) {
      users_filter = { DepartmentId : department_id };
    } else {
      department_id = undefined;
    }

    var company = await req.user.getCompany({
      include : [
        {
          model    : model.User,
          as       : 'users',
          where    : users_filter,
          required : false,
          include  : [
            {
              model: model.Department,
              as: 'department',
              required: false,
            },
          ],
        },
      ],
    })
    return company
}

router.post('/submit', async function(req, res){
  var company = await getAllUsers(req)
  var successCount = 0
  var errorCount = 0
  for (var user of company.users) {
	  var template = handlebars.compile(req.body.body)
    var templatedText = template({
      name: `${user.name} ${user.lastname}`,
      department: user.department.name,
    })

    try {
      //TODO: Implement email sending functionality
      throw Error("Email functionality not implemented yet");

      successCount += 1
    } catch (err) {
      errorCount += 1
    }
  }

  req.session.flash_message(`Email successfully sent to ${successCount} users. ${errorCount} emails failed to send.`)
  return res.redirect_with_session('/email')
});

module.exports = router;

