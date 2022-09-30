const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))

function activatePlacesSearch() {
    var options = {
        types: ['(cities)'],
    };
    var input = document.getElementById('location');
    var autocomplete = new google.maps.places.Autocomplete(input, options)

    google.maps.event.addListener(autocomplete, 'place_changed', function() {
        var place = autocomplete.getPlace();
        var place_id = place.place_id
        var latitude = place.geometry.location.lat();
        var longitude = place.geometry.location.lng();
        $('#location_id').val(place_id)
        $('#longitude').val(longitude)
        $('#latitude').val(latitude)
    });
}

class CustomSelect {
    constructor(originalSelect) {
        this.originalSelect = originalSelect;
        this.customSelect = document.createElement("div");
        this.customSelect.classList.add("select");

        this.originalSelect.querySelectorAll("option").forEach(optionElement => {
            const itemElement = document.createElement("button");

            itemElement.classList.add("btn");
            itemElement.classList.add("btn-outline-primary");
            itemElement.classList.add("btn-sm");
            itemElement.classList.add("me-1");
            itemElement.classList.add("mt-1");
            itemElement.setAttribute("data-bs-toggle", "button");
            itemElement.textContent = optionElement.textContent;
            this.customSelect.appendChild(itemElement);

            if (optionElement.selected) {
                this._select(itemElement);
            }

            itemElement.addEventListener("click", () => {
                if (itemElement.classList.contains("active")) {
                    this._select(itemElement);
                } else {
                    this._deselect(itemElement);
                }
            });
        });

        this.originalSelect.insertAdjacentElement("afterend", this.customSelect);
        this.originalSelect.style.display = "none";
    }

    _select(itemElement) {
        const index = Array.from(this.customSelect.children).indexOf(itemElement);

        if (!this.originalSelect.multiple){
            this.customSelect.querySelectorAll(".btn").forEach(el => {
                el.setAttribute("aria-pressed", "false");
                el.classList.remove("active")
            });
            itemElement.setAttribute("aria-pressed", true);
            itemElement.classList.add("active")
        }

        this.originalSelect.querySelectorAll("option")[index].selected = true;
        itemElement.setAttribute("aria-pressed", true);
        itemElement.classList.add("active")
    }

    _deselect(itemElement) {
        const index = Array.from(this.customSelect.children).indexOf(itemElement);

        this.originalSelect.querySelectorAll("option")[index].selected = false;
    }
}

document.querySelectorAll(".custom-select").forEach(selectElement => {
    new CustomSelect(selectElement);
});

var croppper;
var imageFile;
var base64ImageString;
var cropX;
var cropY;
var cropWidth;
var cropHeight;

function isImageSizeValid(image){
    var startIndex = image.indexOf('base64,') + 7
    var base64str = image.substring(startIndex)
    return base64str
}

function cropImage(image, x, y, width, height){
    base64ImageString = isImageSizeValid(image)
    console.log(csrfToken)
    console.log(urlId)
    var requestData = {
        'csrfmiddlewaretoken': csrfToken,
        'image': base64ImageString,
        'cropX': cropX,
        'cropY': cropY,
        'cropWidth': cropWidth,
        'cropHeight': cropHeight,
    }
    displayLoadingSpinner(true)
    $.ajax({
        type: 'POST',
        dataType: 'json',
        url: urlId,
        data: requestData,
        timeout: 10000,
        success: function (data){
            if(data.result == 'success'){
                document.getElementById("id_cancel").click()
            } else if(data.result == 'error'){
                alert(data.exception)
                document.getElementById("id_cancel").click()
            }
        },
        error: function (data){
            console.error('ERROR!!!!!!!!', data)
        },
        complete: function (data){
            displayLoadingSpinner(false)
        }

    })

}

function setImageCropProperties(image, x, y, width, height){
    imageFile = image
    cropX = x
    cropY = y
    cropWidth = width
    cropHeight = height
}

function readURL(input){
    if(input.files && input.files[0]){
        var reader = new FileReader()

        reader.onload = function (e){
            disableImageOverlay()
            var image = e.target.result
            var profileImage = document.getElementById("id_profile_image")
            profileImage.src = image
            croppper = new Cropper(profileImage, {
                aspectRatio: 1/1,
                crop(event) {
                    setImageCropProperties(
                        image,
                        event.detail.x,
                        event.detail.y,
                        event.detail.width,
                        event.detail.height,
                    )
                }
            })
        };

        reader.readAsDataURL(input.files[0])
    }
}

function overMouseOverlay(event){
    var profileImage = document.getElementById("id_profile_image")
    var middleContainer = document.getElementById("id_middle_container")
    profileImage.style.opacity = "0.3"
    middleContainer.style.opacity = "1"
}

function outMouseOverlay(event){
    var profileImage = document.getElementById("id_profile_image")
    var middleContainer = document.getElementById("id_middle_container")
    profileImage.style.opacity = "1"
    middleContainer.style.opacity = "0"
}

function clickImageContainer(event){
    document.getElementById("id_profile_image_file_selector").click()
}

function enableImageOverlay(){
    var text = document.getElementById("id_text")
    text.style.backgroundColor = "#0d6efc"
    text.style.color = "white"
    text.style.fontSize = "16px"
    text.style.padding = "16px 32px"
    text.style.cursor = "pointer"

    var profileImageSelector = document.getElementById("id_profile_image_file_selector")
    profileImageSelector.style.opacity = "1"
    profileImageSelector.style.display = "block"
    profileImageSelector.style.width = "100%"
    profileImageSelector.style.height = "auto"
    profileImageSelector.style.transition = ".5s ease"
    profileImageSelector.style.backfaceVisibility = "hidden"
    profileImageSelector.style.cursor = "pointer"

    var middleContainer = document.getElementById("id_middle_container")
    middleContainer.style.opacity = "0"
    middleContainer.style.position = "absolute"
    middleContainer.style.top = "20%"
    middleContainer.style.left = "50%"
    middleContainer.style.transform = "translate(-50%, -50%)"

    var imageContainer = document.getElementById("id_image_container")
    imageContainer.addEventListener("mouseover", overMouseOverlay)

    imageContainer.addEventListener("mouseout", outMouseOverlay)

    imageContainer.addEventListener("click", clickImageContainer)

    var cropConfirm = document.getElementById("id_image_crop_confirm")
    cropConfirm.classList.remove("d-flex")
    cropConfirm.classList.remove("flex-row")
    cropConfirm.classList.remove("justify-content-between")
    cropConfirm.classList.add("d-none")
}

function disableImageOverlay(){
    var profileImage = document.getElementById("id_profile_image")
    var profileImageSelector = document.getElementById("id_profile_image_file_selector")
    var middleContainer = document.getElementById("id_middle_container")
    var imageContainer = document.getElementById("id_image_container")
    var text = document.getElementById("id_text")

    imageContainer.removeEventListener("mouseover", overMouseOverlay)
    imageContainer.removeEventListener("mouseout", outMouseOverlay)

    profileImage.style.opacity = "1"
    middleContainer.style.opacity = "0"
    text.style.cursor = "default"
    text.style.opacity = "0"

    imageContainer.removeEventListener("click", clickImageContainer)

    profileImage.addEventListener("click", function (event){
        event.preventDefault()
    })

    var cropConfirm = document.getElementById("id_image_crop_confirm")
    cropConfirm.classList.add("d-flex")
    cropConfirm.classList.add("flex-row")
    cropConfirm.classList.add("justify-content-between")
    cropConfirm.classList.remove("d-none")

    var confirm = document.getElementById("id_confirm")
    confirm.addEventListener("click", function (event){
        cropImage(imageFile, cropX, cropY, cropWidth, cropHeight)
    })

    var cancel = document.getElementById("id_cancel")
    cancel.addEventListener("click", function (event){
        window.location.reload()
    })
}

function displayLoadingSpinner(isDisplayed){
    var spinner = document.getElementById("id_loading_spinner")
    if(isDisplayed){
        spinner.style.display = "block"
    }else{
        spinner.style.display = "none"
    }
}