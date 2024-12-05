let currentSlide = 0; // 當前顯示的圖片索引
const slides = document.querySelectorAll('.slides img'); // 選擇所有圖片
const totalSlides = slides.length; // 總圖片數
console.log(`totalSlides: ${totalSlides}`); // 測試用，確認圖片數量是否正確

function updateSlide() {
  const slidesContainer = document.querySelector('.slides');
  const gap = 100;
  slidesContainer.style.transform = `translateX(calc(-${currentSlide * 100}% - ${currentSlide * gap}px))`; // 移動到對應的圖片
}     // 先使用calc(css計算語法)說後面要計算 //${ } JS 表達式

function prevSlide(){
  if (currentSlide === 0 ){
    currentSlide = totalSlides - 1;
  }else{
    currentSlide = currentSlide -1;
  }
  console.log(`currentSlide: ${currentSlide}`); // 測試用，確認是否更新正確
  updateSlide();
}
//function prevSlide() {
  //currentSlide = (currentSlide === 0) ? totalSlides - 1 : currentSlide - 1; // 循環到最後一張
  //updateSlide();
//}

function nextSlide() {
  currentSlide = (currentSlide === totalSlides - 1) ? 0 : currentSlide + 1; // 循環到第一張
  updateSlide();
}
