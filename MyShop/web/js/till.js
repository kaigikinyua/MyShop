var items=[]


function addItem(){
    itemName=document.getElementById('itemCode').value
    quantity=document.getElementById('quantity').value
    price=100
    total=price*quantity
    items.push({'name':itemName,'price':200,'quantity':quantity,'total':total})
    var itemParent=document.getElementById('itemList')
    var itemDiv=document.createElement('div')
    itemDiv.classList.add('item')
    itemDiv.id='item'+items.length
    itemDiv.innerHTML=itemName+' @200 *'+quantity+' ='+total
    itemParent.appendChild(itemDiv)

}
function removeItem(itemId){
    items.pop(itemId)
}

function computeTotal(){}

