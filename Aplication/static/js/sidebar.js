let btn = document.querySelector('#btn');
let sidebar = document.querySelector('.sidebar');
let srcBtn = document.querySelector('.bx-search');

btn.onclick = function(){
    sidebar.classList.toggle('active');
}
srcBtn.onclick = function(){
    sidebar.classList.toggle('active');
}