document.addEventListener("DOMContentLoaded", function() {
	for (let fieldElem of document.querySelectorAll('.choices-js-field')) {
		let options = {};
		if (fieldElem.dataset.choicesJs) {
			options = JSON.parse(fieldElem.dataset.choicesJs);
		}
		const choices = new Choices(fieldElem, options);
		if (fieldElem.dataset.choicesJsAutocomplete) {
			choices.passedElement.element.addEventListener('search', async (e) => {
				const searchParams = new URLSearchParams({q: e.detail.value});
				const path = fieldElem.dataset.choicesJsAutocomplete;
				const response = await fetch(`/django_choices_js/autocomplete/${path}.json?${searchParams.toString()}`).then(res => res.json());
				choices.setChoices(response.choices, 'value', 'label', true);
 			});
		}
	}
});
