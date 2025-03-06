const searchFiled = document.querySelector('#searchFiled');

searchFiled.addEventListener('keyup', (e)=>{
    const searchValue = e.target.value.toLowerCase();
    if(searchValue.length >0){
        console.log(searchValue)
    }
});