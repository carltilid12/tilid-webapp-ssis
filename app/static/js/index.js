// Search Script
$(document).ready(function() {
    // Listen for changes in the search input field
    $("#search-input").on("input", function() {
        var searchText = $(this).val().toLowerCase();

        // Loop through table rows and hide those that don't match the search text
        $(".highlightable-row").each(function() {
            // Get all td elements except the last one
            var tdsToSearch = $(this).find('td:not(:last-child)');
            
            // Concatenate the text content of each td
            var rowText = tdsToSearch.map(function() {
                return $(this).text().toLowerCase();
            }).get().join(' ');

            // Check if the rowText contains the search text
            if (rowText.indexOf(searchText) === -1) {
                $(this).hide();
            } else {
                $(this).show();
            }
        });
    });
});

// Table Highlight Script
$(document).ready(function () {
    // Add hover event listener to highlight rows on hover
    $(".highlightable-row").hover(
        function () {
            // Mouse enter
            $(this).addClass("table-active");
            $(this).find(".edit-btn, .delete-btn").show();
        },
        function () {
            // Mouse leave
            $(this).removeClass("table-active");
            $(this).find(".edit-btn, .delete-btn").hide();
        }
    );
});