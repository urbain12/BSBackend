/**
 * Created by alainkajangwe on 23/11/16.
 */


$('#btnSubmitId').on('click', function(event) {
    event.preventDefault();

    var currentForm = $(this).closest('form');

    var dataValue = $(this).data('value');
    console.log(dataValue);
    var confirmMessage = dataValue;

    bootbox.confirm({
        message: confirmMessage,
        callback: function (result) {
            if (result) {
                /*
                 $.niftyNoty({
                 type: 'success',
                 icon : 'pli-like-2 icon-2x',
                 container : 'floating',
                 message : 'User confirmed dialog',
                 timer : 5000
                 });
                 */
                currentForm.unbind('submit').submit();

            } else {
                /*
                 $.niftyNoty({
                 type: 'danger',
                 icon : 'pli-cross icon-2x',
                 message : 'User declined dialog.',
                 container : 'floating',
                 timer : 5000
                 });
                 */
            }
            ;
        }
    });

});

/*
 $('#activeFormId').validator().on('submit', function (e) {
 if (e.isDefaultPrevented()) {
 console.log('handle the invalid form...');
 } else {
 console.log('everything looks good!');
 }
 });
 */

/*
 $('#btnSubmitId').on('click', function(event) {
 event.preventDefault();

 var currentForm = $(this).closest('form');
 // var allInputs = $("#activeFormId input");
 var allInputs = currentForm.find('input');
 var errors = [];
 var data = currentForm.serializeArray();

 console.log('inputs : ' + allInputs.length);

 for(var i=0; i<data.length-1; i++){
 if(data[i].value.length == 0){
 if ($(allInputs)[i] != undefined) {
 var currErrorDiv = $(allInputs)[i].closest('.has-error'); // this will give the corresponding div of the empty field input
 console.log(currErrorDiv);

 if (currErrorDiv != null)
 errors.push(currErrorDiv);
 }
 }
 }
 console.log('number of errors: ' + errors.length);

 if (errors.length == 0) {
 var dataValue = $(this).data('value');
 console.log(dataValue);
 var confirmMessage = dataValue;

 bootbox.confirm({
 message: confirmMessage,
 callback: function (result) {
 if (result) {

 currentForm.unbind('submit').submit();

 }
 ;
 }
 });

 } else {
 console.log('Form Validation Failed!');

 }
 });
 */

/*
 $('#btnMemberUpdateId').on('click', function(){
 event.preventDefault();
 var currentForm = $(this).closest('form');

 var list = '';
 var email = $('#member-email').val();
 var lastname = $('#member-last_name').val();
 var firstname = $('#member-first_name').val();
 var birthday = $('#member-birthday').val();
 var post_code = $('#member-post_code').val();
 var prefecture = $('#member-prefecture').val();
 var city = $('#member-city').val();
 var addr1 = $('#member-address1').val();
 var addr2 = $('#member-address2').val();
 var sex = $('#member-sex').val();
 var phone = $('#member-phone').val();
 var status = $('#member-status').val();
 var rank = $('#member-member_rank_id').val();
 var bank_status = $('#member-bank_account_status').val();
 var address_check = $('#member-address_reality_check').val();
 var initial_payment = $('#member-initial_payment').val();
 var mobile = $('#member-mobile').val();
 var nickname = $('#member-nickname').val();


 list += '<div class="panel">';
 list += '<div class="panel-body">';
 list += '<div class="panel-heading">';
 list += '<h3 class="panel-title">' + 'Member update confirmation' + '</h3>';
 list += '</div>';
 list += '<table class="table table-striped table-bordered table-hover table-condensed">';

 list += '<tr>';
 list += '<td>Email: </td>';
 list += '<td>'+email+'</td>';
 list += '</tr>';

 list += '<tr>';
 list += '<td>Lastname: </td>';
 list += '<td>'+lastname+'</td>';
 list += '</tr>';

 list += '<tr>';
 list += '<td>Firstname: </td>';
 list += '<td>'+firstname+'</td>';
 list += '</tr>';

 list += '<tr>';
 list += '<td>Birthday: </td>';
 list += '<td>'+birthday+'</td>';
 list += '</tr>';

 list += '<tr>';
 list += '<td>Post Code: </td>';
 list += '<td>'+post_code+'</td>';
 list += '</tr>';

 list += '<tr>';
 list += '<td>Prefecture: </td>';
 list += '<td>'+prefecture+'</td>';
 list += '</tr>';

 list += '<tr>';
 list += '<td>City: </td>';
 list += '<td>'+city+'</td>';
 list += '</tr>';

 list += '<tr>';
 list += '<td>Address1: </td>';
 list += '<td>'+addr1+'</td>';
 list += '</tr>';

 list += '<tr>';
 list += '<td>Address2: </td>';
 list += '<td>'+addr2+'</td>';
 list += '</tr>';

 list += '<tr>';
 list += '<td>Sex: </td>';
 list += '<td>'+sex+'</td>';
 list += '</tr>';

 list += '<tr>';
 list += '<td>Phone: </td>';
 list += '<td>'+phone+'</td>';
 list += '</tr>';

 list += '<tr>';
 list += '<td>Status: </td>';
 list += '<td>'+status+'</td>';
 list += '</tr>';

 list += '<tr>';
 list += '<td>Member Rank: </td>';
 list += '<td>'+rank+'</td>';
 list += '</tr>';

 list += '<tr>';
 list += '<td>Bank Account Status: </td>';
 list += '<td>'+bank_status+'</td>';
 list += '</tr>';

 list += '<tr>';
 list += '<td>Address Reality Check: </td>';
 list += '<td>'+address_check+'</td>';
 list += '</tr>';

 list += '<tr>';
 list += '<td>Initial Payment: </td>';
 list += '<td>'+initial_payment+'</td>';
 list += '</tr>';

 list += '<tr>';
 list += '<td>Mobile: </td>';
 list += '<td>'+mobile+'</td>';
 list += '</tr>';

 list += '<tr>';
 list += '<td>Nickname: </td>';
 list += '<td>'+nickname+'</td>';
 list += '</tr>';

 list += '</table>';
 list += '</div>';
 list += '</div>';

 bootbox.confirm({
 message: list,
 callback: function(result){
 if (result) {
 $.niftyNoty({
 type: 'success',
 icon : 'pli-like-2 icon-2x',
 // message : 'User confirmed dialog',
 container : 'floating',
 timer : 5000
 });
 currentForm.unbind('submit').submit();

 }else{
 $.niftyNoty({
 type: 'danger',
 icon : 'pli-cross icon-2x',
 message : 'User declined dialog.',
 container : 'floating',
 timer : 5000
 });
 };

 }

 });
 });
 */