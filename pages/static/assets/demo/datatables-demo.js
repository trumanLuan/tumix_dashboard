// Call the dataTables jQuery plugin
$(document).ready(function() {
  var table = $('#dataTable').DataTable({
    select: {
        style: 'single'
    }
  });

  $('#dataTable tbody').on('click','tr', function(){
         var data = table.row(this).data()[0];
         console.log(data);
        // 在此处执行您希望的操作，例如将时间发送到服务器或执行其他逻辑
     });
});
