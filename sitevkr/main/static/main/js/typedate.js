$(function () {
        $("input[name='type_date']").click(function () {
            if ($("#radio_day").is(":checked")) {
                $("#select_day").show();
                $("#date_day_div").show();

                if ($('#select_day').val() == 'sd1'){
                    $("#check_graph_day_div").show();
                } else {
                    $("#check_graph_day_div").hide();
//                    $("#check_graph_day").prop("checked", false);
                }

            } else {
                $("#select_day").hide();
                $("#check_graph_day_div").hide();
                $("#date_day_div").hide();


            }

            if ($("#radio_month").is(":checked")) {
                  $("#select_month").show();
                  $("#date_month_div").show();

                   if ($('#select_month').val() == 'sm2' ){
                    $("#check_graph_month_div").show();
                 } else {
                    $("#check_graph_month_div").hide();
//                    $("#check_graph_month").prop("checked", false);
                 }

            } else {
                $("#select_month").hide();
                $("#check_graph_month_div").hide();
                $("#date_month_div").hide();

            }

            if ($("#radio_year").is(":checked")) {
                  $("#select_year").show();

                  if ($('#select_year').val() == 'sy3'){
                    $("#check_graph_year_div").show();
                 } else {
                    $("#check_graph_year_div").hide();
//                    $("#check_graph_year").prop("checked", false);
                 }

            } else {
                $("#select_year").hide();
                $("#check_graph_year_div").hide();
            }

            if ($("#radio_custom").is(":checked")) {
                 $("#select_custom").show();
                 $("#date_custom_div").show();

            } else {
                 $("#select_custom").hide();
                 $("#date_custom_div").hide();
            }
        });
    });

$(function () {
    $( "#select_day" ).change(function() {
        if ($('#select_day').val() == 'sd1'){
                $("#check_graph_day_div").show();
        } else {
                $("#check_graph_day_div").hide();
//                $("#check_graph_day").prop("checked", false);
        }
    });

    $( "#select_month" ).change(function() {
        if ($('#select_month').val() == 'sm2'){
                $("#check_graph_month_div").show();
        } else {
                $("#check_graph_month_div").hide();
//                $("#check_graph_month").prop("checked", false);
        }
    });

    $( "#select_year" ).change(function() {
        if ($('#select_year').val() == 'sy3'){
                $("#check_graph_year_div").show();
        } else {
                $("#check_graph_year_div").hide();
//                $("#check_graph_year").prop("checked", false);
        }
    });
});



