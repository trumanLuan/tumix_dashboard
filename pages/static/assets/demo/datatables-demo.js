// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').dataTable({
    "pagingType": "full_numbers",
    // 在dataTable内某一列添加自定义按钮
    "columnDefs":[
        {
        // targets用于指定操作的列，从第0列开始，-1为最后一列
        // returns后是我们希望在指定列填入的按钮代码
           "targets":-1,
           "render": function(data, type, full, meta){
                return  "<input type = 'button' id = 'checkBrowseResButton' value = 'Check'>"
           }
        }
    ]
//    "columns": [
//                    { "data": "studyIndex" },
//                    { "data": "studySpecies" },
//                    { "data": "studyTumorSite" },
//                    { "data": "studyNdonor" },
//                    { "data": "studyNsample" },
//                    { "data": "studyNcell" },
//                    { "data": "studyNtumorCell" },
//                    { "data": "studySorting" },
//                    { "data": "studyTreatment" },
//                    { "data": null}
//                ]
  });
/*
  $('#dataTable tbody').on('click','#checkBrowseResButton', function(){
          // 获取行
         var row = $("#dataTable tr").index($(this).closest("tr"));
         // 获取某列（从0列开始计数）的值
         var index = $("#dataTable").find("tr").eq(row).find('td').eq(0).text();
        // 在此处执行您希望的操作，例如将时间发送到服务器或执行其他逻辑
        alert("You chose " + index);
     });*/

     $('#dataTable tbody tr') .live('click', function() {
         var  data = table.row(  this  ).data();
         alert(  'You clicked on ' + data[0] + '\'s row'  );
     } );
});
