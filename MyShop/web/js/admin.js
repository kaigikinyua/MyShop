const windows=['reportsWindow','stockWindow','usersWindow','productsWindow']
function viewWindow(windowId){
    windows.forEach(w=>{
        //console.log(w)
        document.getElementById(w).style.display='none'
    })
    document.getElementById(windowId).style.display=''
}

class PopUpWindow{
    static addProduct(){

    }
}

class AdminFetchDataItems{
    static async getProducts(){
        var products=await eel.getAllProducts()()
        return products
    }
}
class RenderItems{

    static renderProduct(product){
        var parent=document.getElementById('productList')
        var pElement=document.createElement('div')
        var pName=document.createElement('p')
        pName.innerHTML=product['name']
        var deleteProduct=document.createElement('button')
        deleteProduct.classList='danger'
        deleteProduct.innerHTML='Delete'
        deleteProduct.onclick=(()=>{
            AdminActions.deleteProduct(product['id'])
        });
    }
}

class AdminActions{
    static getUserId(){
        var id=getUserId()
    }
    static async deleteProduct(productId){
        var userId=AdminActions.getUserId()
        var result=await eel.deleteProduct(userId,productId)();
        if(result){

        }
    }
}

function getAndRenderProducts(){
    var products=AdminFetchDataItems.getProducts()
    products.forEach((product)=>{

    })
}

function setUpAdmin(){

}