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


$("document").ready(function () {

//alert(selectedOption.value);
    console.log('I founf Jquert first');
    $(".classSelect").change(function () {
        let selectedOption = mySelect.options[mySelect.selectedIndex];
        console.log("We found just mySelect!!!!", selectedOption.value);
})
})


$("document").ready(function () {
    $(".form-control").change(function() {
        console.log("And we found form-control");
        let selectYear = year.options[year.selectedIndex].value;
        let selectFinanceCost = financeCost.options[financeCost.selectedIndex].value;
        let selectCurator = curator.options[curator.selectedIndex].value;
        let selectContractType = contractType.options[contractType.selectedIndex].value;
        let selectContractStatus = contractStatus.options[contractStatus.selectedIndex].value;
        console.log("Выбранный год", selectYear);
        console.log("Выбранная статья финансирования", selectFinanceCost);
        console.log("Выбранная куратор", selectCurator);

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


$("#report").click(function () {
    var my_options = $("#report option");

    my_options.sort(function(a,b) {
            return a.text.slice(0,2) - b.text.slice(0,2);
        });
    console.log("Hello from sort");
    console.log(my_options);
    $("#report").empty().append(my_options);
});




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
}

function makePDF() {

    var quotes = document.getElementById('HTMLtoPDF');

    html2canvas(quotes, {
        onrendered: function(canvas) {

        //! MAKE YOUR PDF
        var pdf = new jsPDF('p', 'pt', 'letter');

        for (var i = 0; i <= quotes.clientHeight/980; i++) {
            //! This is all just html2canvas stuff
            var srcImg  = canvas;
            var sX      = 0;
            var sY      = 980*i; // start 980 pixels down for every new page
            var sWidth  = 900;
            var sHeight = 980;
            var dX      = 0;
            var dY      = 0;
            var dWidth  = 900;
            var dHeight = 980;

            window.onePageCanvas = document.createElement("canvas");
            onePageCanvas.setAttribute('width', 900);
            onePageCanvas.setAttribute('height', 980);
            var ctx = onePageCanvas.getContext('2d');
            // details on this usage of this function:
            // https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Using_images#Slicing
            ctx.drawImage(srcImg,sX,sY,sWidth,sHeight,dX,dY,dWidth,dHeight);

            // document.body.appendChild(canvas);
            var canvasDataURL = onePageCanvas.toDataURL("image/png", 1.0);

            var width         = onePageCanvas.width;
            var height        = onePageCanvas.clientHeight;

            //! If we're on anything other than the first page,
            // add another page
            if (i > 0) {
                pdf.addPage(612, 791); //8.5" x 11" in pts (in*72)
            }
            //! now we declare that we're working on that page
            pdf.setPage(i+1);
            //! now we add content to that page!
            pdf.addImage(canvasDataURL, 'PNG', 20, 40, (width*.62), (height*.62));

        }
        //! after the for loop is finished running, we save the pdf.
        pdf.save('implementationReport.pdf');
    }
  });
}





