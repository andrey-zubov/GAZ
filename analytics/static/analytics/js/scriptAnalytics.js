//Значения форм 1 и 2 отчета по умолчанию
$("document").ready(function(){
        console.log("hello")
        $("#curator").val(1)
        $("#financeCost").val(1)
        $("#year").val(2020)
        $("#report").val(1)
        $("#contractType").val(0)
        $("#contractStatus").val(0)

    }
)

//Первый отчет: фильтрация без перезагрузки страницы
$("document").ready(function () {
    $(".form-implementation").change(function() {
        let selectYear = year.options[year.selectedIndex].value;
        let selectFinanceCost = financeCost.options[financeCost.selectedIndex].value;
        let selectCurator = curator.options[curator.selectedIndex].value;
        let selectContractType = contractType.options[contractType.selectedIndex].value;
        let selectContractStatus = contractStatus.options[contractStatus.selectedIndex].value;

        $.ajax({
            'url':"/analytics/implementation_plan/",
            "data": {
                'select_year': selectYear,
                'select_cost':selectFinanceCost,
                'select_curator': selectCurator,
//                'select_report': 1
                'select_contractType': selectContractType,
                'select_contractStatus': selectContractStatus

            },
            dataType:'html',
            "success": function(data) {
                $("#reportName").html($(data).find("#reportName"));
                $("#table_id").html($(data).find("#table_id"));
                $("#scriptIDmyChart").html($(data).find("#scriptIDmyChart"));
                $("#scriptIDcontractCountAll").html($(data).find("#scriptIDcontractCountAll"));
                $("#scriptIDcontractCountSub").html($(data).find("#scriptIDcontractCountSub"));
                $("#scriptIDcontractCountCentre").html($(data).find("#scriptIDcontractCountCentre"));
                $("#myChart").html($(data).find("#myChart"));
                $("#contractCountAll").html($(data).find("#contractCountAll"));
                $("#contractCountSub").html($(data).find("#contractCountSub"));
                $("#contractCountCentre").html($(data).find("#contractCountCentre"));

            }
        })
    })
})


//Второй отчет: сортировка отчетов формы
$("#report").click(function () {
    var my_options = $("#report option");

    my_options.sort(function(a,b) {
            return a.text.slice(0,2) - b.text.slice(0,2);
        });
    console.log("Hello from sort");
    console.log(my_options);
    $("#report").empty().append(my_options);
});


//Второй отчет: фильтрация без перезагрузки страницы
$("document").ready(function () {
    console.log("Deviation")
    $(".form-deviation").change(function() {
        let selectYear = year.options[year.selectedIndex].value;
        let selectFinanceCost = financeCost.options[financeCost.selectedIndex].value;
        let selectCurator = curator.options[curator.selectedIndex].value;
        let selectReport = report.options[report.selectedIndex].value;
        console.log("From data ", selectYear, selectFinanceCost, selectCurator, selectReport)
        $.ajax({
            'url':"/analytics/deviation_analysis/",
            "data": {
                'select_year': selectYear,
                'select_cost':selectFinanceCost,
                'select_curator': selectCurator,
                'select_report': selectReport
            },
            dataType:'html',
            "success": function(data) {
                $("#deviationName").html($(data).find("#deviationName"));
                $("#tableDeviation").html($(data).find("#tableDeviation"));
                $("#deviationChartScript").html($(data).find("#deviationChartScript"));
                $("#mdeviationChart").html($(data).find("#deviationChart"));


            }
        })
    })
})

//Для всех отчетов: экспорт в Excel
function exportToExcel(tableID, filename = ''){
    var downloadurl;
    var dataFileType = 'application/vnd.ms-excel;charset=UTF-8';
    var tableSelect = document.getElementById(tableID);
    var tableHTMLData = tableSelect.outerHTML.replace(/ /g, '%20');

    // Specify file name
    filename = filename?filename+'.xls':'export_excel_data.xls';

    // Create download link element
    downloadurl = document.createElement("a");

    document.body.appendChild(downloadurl);

    if(navigator.msSaveOrOpenBlob){
        var blob = new Blob(['\ufeff', tableHTMLData], {
            type: dataFileType
        });
        navigator.msSaveOrOpenBlob( blob, filename);
    }else{
        // Create a link to the file
        downloadurl.href = 'data:' + dataFileType + ', ' + tableHTMLData;

        // Setting the file name
        downloadurl.download = filename;

        //triggering the function
        downloadurl.click();
    }
};


//Выпадающее меню для PDF, Excel

/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {

    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}


//   PDF for all reports
function generatePDF() {
        // Choose the element that our invoice is rendered in.
        const element = document.getElementById("HTMLtoPDF");
        const form = document.getElementById("form")
        const opt = {
        html2canvas: {scale:2, ignoreElements:form},
        jsPDF: {unit:'mm', format:'a4', orientation: 'l'}};
        // Choose the element and save the PDF for our user.
        html2pdf()
          .set(opt)
          .from(element)
          .save();
      }

//3 Отчет, Drag and drop
// Sortable column heads
var oldIndex;
$('.sorted_head tr').sortable({
  containerSelector: 'tr',
  itemSelector: 'th',
  placeholder: '<th class="placeholder"/>',
  vertical: false,
  onDragStart: function ($item, container, _super) {
    oldIndex = $item.index();
    $item.appendTo($item.parent());
    _super($item, container);
  },
  onDrop: function  ($item, container, _super) {
    var field,
        newIndex = $item.index();

    if(newIndex != oldIndex) {
      $item.closest('table').find('tbody tr').each(function (i, row) {
        row = $(row);
        if(newIndex < oldIndex) {
          row.children().eq(newIndex).before(row.children()[oldIndex]);
        } else if (newIndex > oldIndex) {
          row.children().eq(newIndex).after(row.children()[oldIndex]);
        }
      });
    }

    _super($item, container);
  }
});
