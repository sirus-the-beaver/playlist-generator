const submit = document.querySelector('input[type="submit"]');
const mood_radios = document.querySelectorAll('input[type="radio"][name="mood"]');
const energy_radios = document.querySelectorAll('input[type="radio"][name="energy"]');
const dance_radios = document.querySelectorAll('input[type="radio"][name="dance"]');

submit.addEventListener('click', function(event) {
    mood_selected = false;
    for (mood_radio of mood_radios) {
        if (mood_radio.checked) {
            mood_selected = true;
        }
    }
    energy_selected = false;
    for (energy_radio of energy_radios) {
        if (energy_radio.checked) {
            energy_selected = true;
        }
    }
    dance_selected = false;
    for (dance_radio of dance_radios) {
        if (dance_radio.checked) {
            dance_selected = true;
        }
    }
    if (!mood_selected) {
        event.preventDefault();
        alert('Please select a mood');
    }

    if (!energy_selected) {
        event.preventDefault();
        alert('Please select an energy level');
    }

    if (!dance_selected) {
        event.preventDefault();
        alert('Please select a danceability');
    }
});