const searchFiled = document.querySelector('#searchFiled');
const tableOutput = document.querySelector('.table-output');
tableOutput.style.display='none';
const appTable = document.querySelector('.app-table');
const paginationContainer = document.querySelector('.pagination-container');
const tableBody=document.querySelector('.table-body');
const noResult = document.querySelector('.no-result')
searchFiled.addEventListener('keyup', (e)=>{
    const searchValue = e.target.value.toLowerCase();
    
    if(searchValue.trim().length >0){
        paginationContainer.style.display ='none';
        tableBody.innerHTML="";
        //console.log(searchValue)
        fetch("/search-expenses",{
            method: 'POST',
            body:JSON.stringify({searchText:searchValue}),
    
        })
        .then(response => response.json())
        .then(data=>{
             //console.log(data);
             tableOutput.style.display='block';
             appTable.style.display='none'; 
             if(data.length===0){ 
                 tableOutput.style.display='none';
                 noResult.style.display='block'
             }else{
                noResult.style.display='none'
                //tableOutput.style.display=;
                console.log(data)
                data.forEach(item => {
                    tableBody.innerHTML+=`
                    <tr>
                            <td>${item.amount}</td>
                            <td>${item.category}</td>
                            <td>${item.description}</td>
                            <td>${item.date}</td>
                           
                    </tr>`;
                });
               
             }
        } );
    }
    else{
        tableOutput.style.display='none';
        appTable.style.display='block'; 
        paginationContainer.style.display ='block';
    }
});