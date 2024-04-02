new Autocomplete('#autocomplete', {
        search: input => {
            const url = `/get-names/?search=${input}`;
            return fetch(url)
                .then(response => response.json())
                .then(data => data.payload);
        },
        renderResult: (result, props) => {
            // Render each result item
            return `<li ${props}><div class='wiki-title'>${result.Name}</div></li>`;
        },
        onSubmit: result => {
            // Display the selected customer name in the input field
            document.querySelector(".autocomplete-input").value = result['Phone Number'];
            // Create label elements
            document.querySelector("#Name").value=result.Name;
            document.querySelector("#Age").value=result.Age;
        }
    });
