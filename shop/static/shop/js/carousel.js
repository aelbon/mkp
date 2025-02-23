window.handleMapClick = function handleMapClick(event) {
  event.preventDefault();
  event.stopPropagation();

  const newIndex = parseInt(event.target.dataset.index);
  const carousel = event.target.closest(".carousel");

  slide(carousel, newIndex);
};

window.slideOne = function slideOne(event, dir) {
  event.preventDefault();
  event.stopPropagation();

  const carousel = event.target.closest(".carousel");
  let maxIndex = carousel.querySelector(".slide-holder").children.length;
  let newIndex = parseInt(carousel.dataset.index) + dir;

  if (newIndex < 0 || newIndex >= maxIndex) {
    return;
  }

  slide(carousel, newIndex);
};

function slide(carousel, index) {
  const holder = carousel.querySelector(".slide-holder");
  const maxIndex = holder.children.length;

  const padding = 10; // gap defined in css
  holder.style.transform = `translateX(calc(${-index * 100}% - ${
    index * padding
  }px))`;

  const counter = carousel.querySelector(".slide-counter");
  counter.innerHTML = `${index + 1}/${maxIndex}`;
  carousel.dataset.index = index;
}

// update preview for when adding images to carousel after dom build
// takes a list of files
window.updatePreview = function updatePreview(carousel, files) {
  const slideMap = carousel.querySelector(".slide-map");
  const holder = carousel.querySelector(".slide-holder");
  const slideInfo = carousel.querySelector(".slide-info");

  holder.innerHTML = "";
  slideMap.innerHTML = "";
  slideInfo.style = "";
  slideInfo.querySelector(".slide-counter").innerHTML = `1/${files.length}`;

  carousel.dataset.index = 0;
  holder.style.transform = `translateX(0%)`;

  for (let i = 0; i < files.length; i++) {
    const imageURL = URL.createObjectURL(files[i]);
    const imgNode = document.createElement("img");
    imgNode.src = imageURL;
    holder.appendChild(imgNode);
    if (slideMap) {
      const mapNode = document.createElement("img");
      mapNode.src = imageURL;
      mapNode.dataset.index = i;
      mapNode.onclick = (event) => handleMapClick(event);
      slideMap.appendChild(mapNode);
    }
  }
};
