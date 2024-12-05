let currentphoto = 0;
const slides = document.querySelectorAll('slides img');
const totalSlides = slides.length;

function updateSlides(){
  currentphoto =document.querySelector('.slides')
  const gap = 100;
  currentphoto.style.transform = `translateX(calc(-${currentphoto * 100}% - ${currentphoto * gap}px));

}
function nextSlides(){
  currentphoto = (currentphoto === totalSlides -1 ) ?  0  :  currentphoto + 1;
  updateSlides()
}

function prevSlides(){
  currentphoto = (currentphoto === 0 ) ? totalSlides -1  : currentphoto - 1;
  updateSlides();
}