
'use strict';

var
    _      = require('underscore'),
    model  = require('../model/db'),
    moment = require('moment');

function LeaveRequest(args) {
    var me = this;

    // Make sure all required data is provided
    _.each(
        [
          'leave_type','from_date','from_date_part',
          'to_date', 'to_date_part', 'reason'
        ],
        function(property){
            if (! _.has(args, property)) {
                throw new Error('No mandatory '+property+' was provided to LeaveRequest constructor');
            }
        }
    );

    // From date should not be bigger then to
    if (moment.utc(args.from_date).toDate() > moment.utc(args.to_date).toDate()){
        throw new Error( 'From date should be before To date at LeaveRequest constructor' );
    }

    _.each(
        [
          'leave_type','from_date','from_date_part',
          'to_date', 'to_date_part', 'reason', 'user'
        ],
        function(property){ me[property] = args[property]; }
    );
}

LeaveRequest.prototype.as_data_object = function(){
    var obj = {},
        me = this;

    _.each(
        [
          'leave_type','from_date','from_date_part',
          'to_date', 'to_date_part', 'reason', 'user'
        ],
        function(property){ obj[property] = me[property]; }
    );

    return obj;
};

LeaveRequest.prototype.is_within_one_day = function(){
    return moment.utc(this.from_date).format('YYYY-MM-DD')
          ===
        moment.utc(this.to_date).format('YYYY-MM-DD');
};

LeaveRequest.prototype._does_fit_with_point = function(leave_day, point_name){
    var return_val = false;

    if (
        (
          moment.utc(leave_day.date).format('YYYY-MM-DD')
            ===
          moment.utc(this[point_name]).format('YYYY-MM-DD')
        )
          &&
        (! leave_day.is_all_day_leave())
          &&
        (String(this[point_name+'_part']) !== String(model.Leave.leave_day_part_all()))
          &&
        (String(leave_day.day_part) !== String(this[point_name+'_part']))
    ) {
        return_val = true;
    }

    return return_val;
};

// Check if start date or end date of current object fits with provided leave_day
// instance.
// By fitting I mean days are the same and both of them are
// halfs of different types.
//
LeaveRequest.prototype.does_fit_with_leave_day = function(leave_day){

    return this._does_fit_with_point(leave_day, 'from_date')
        ||
        this._does_fit_with_point(leave_day, 'to_date');
};

LeaveRequest.prototype.does_fit_with_leave_day_at_start = function(leave_day){

    return this._does_fit_with_point(leave_day, 'from_date');
};

LeaveRequest.prototype.does_fit_with_leave_day_at_end = function(leave_day){

    return this._does_fit_with_point(leave_day, 'to_date');
};


module.exports = LeaveRequest;
