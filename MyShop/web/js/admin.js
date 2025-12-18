const windows=['reportsWindow','usersWindow','productsWindow']
function viewWindow(windowId){
    windows.forEach(w=>{
        //console.log(w)
        document.getElementById(w).style.display='none'
    })
    document.getElementById(windowId).style.display=''
}
class ReportsActions{
    static async getXReport(){
        var shiftId=Auth.getShiftId()
        var userId=Auth.getUserId()
        var response=await eel.generateXReport(userId,shiftId)()
        if(response['state']==true){
            return response
        }else{
            notificationBubble(response['message'],0,5)
            return response
        }
    }
    static async getZreport(){
        var shiftId=Auth.getShiftId()
        var userId=Auth.getUserId()
        var response=await eel.generateZReport(userId,shiftId)()
        if(response['state']==true){
            return response
        }else{
            notificationBubble(response['message'],0,5)
            return response
        }
    }

    static async genCreditReport(){
        var shiftId=Auth.getShiftId()
        var userId=Auth.getUserId()
        var response=await eel.generateCreditReport(userId)()
        if(response['state']==true){
            return response
        }else{
            notificationBubble(response['message'],0,5)
            return response
        }
    }
    static async getReportByName(reportName,startDate,endDate){
        
    }
}

class ProductActions{
    static addProduct(){

    }
    static async deleteProduct(productId){
        var userId=AdminActions.getUserId()
        var result=await eel.deleteProduct(userId,productId)();
        if(result){

        }
    }
    
}

class AdminFetchDataItems{
    static async getProducts(){
        var products=await eel.getAllProducts()()
        return products
    }
}

//redundant Auth class and methods in till.js and admin.js
class Auth{
    static renderShiftId(){
        var shiftId=Auth.getShiftId()
        var x=document.getElementById("shiftId")
        x.innerHTML="Shift "+shiftId+" | "
    }
    static getUserId(){
        var token=localStorage.getItem('token')
        var splitToken=token.split(':')
        return splitToken[splitToken.length-1]
    }
    static getShiftId(){
        var shiftId=localStorage.getItem('shiftId')
        if(shiftId!=null && shiftId!=undefined){
            return shiftId
        }else{return 'UnknownShiftId'}
    }
}

function setUpAdmin(){
    Auth.renderShiftId()
}
setTimeout(async ()=>{
    setUpAdmin()
},1000)



//*******VUE APP **********/
const reportsComponent ={
  template: `
    <div class="col1">
        <h3>Reports</h3>
        <div>
            <input type="date" name="startDate" id="startDate_reports" placeholder="13/10/2020"/>
            <input type="date" name="endDate" id="endDate_reports"/>
            <button>X Report</button>
            <button>Z Report</button>
            <button @click='creditReport'>Credit Report</button>
            <button @click='salesReport'>Sales Report</button>
            <button @click='stockReport'>Stock Report</button>
        </div>
    </div>
    <div class="col2" id="reportContent">
        {{title}}
        <xzcomponent :test_data="From"/>
    </div>
  `,
  props:{
    test_data:"componentONe"
  },
  data(){
    return {
        title:'Report Name',
        reportContents:[],
        exportToExcelSheet:false
    }
  },
  methods:{
    xReport(){},
    zReport(){},
    creditReport(){
        var dates=this.getStartAndEndDate()
        this.test_data='changed the props'
        if(dates!=undefined){
            console.log('creditReport between '+dates.start+" to "+dates.end)
        }else{
            console.log('please enter the start date and end date')
        }
    },
    salesReport(){
        var dates=this.getStartAndEndDate()
        if(dates!=undefined){
            console.log('sales Report between '+dates.start+" to "+dates.end)
        }else{
            console.log('please enter the start date and end date')
        }
    },
    stockReport(){
        var dates=this.getStartAndEndDate()
        if(dates!=undefined){
            console.log('sales Report between '+dates.start+" to "+dates.end)
        }else{
            console.log('please enter the start date and end date')
        }
    },
    getStartAndEndDate(event){
        var sDate=document.getElementById('startDate_reports').value;
        var eDate=document.getElementById('endDate_reports').value;
        if(sDate!='' && sDate!=undefined && eDate!='' && sDate!=undefined){
            return {'start':sDate,'end':eDate}
        }else{
            notificationBubble("Please fill in the dates",0,4);
        }
        return undefined
    },
  },
};

const XZComponent={
    props:{
        test_data:undefined
    },
    data(){
        return {
        }
    },
    template:`
        <h3>Component 2</h3>
        <p>{{test_data}}</p>
    `
}




const app=Vue.createApp({})
app.component('xzcomponent',XZComponent)
app.component('reports-component',reportsComponent)
app.mount('#reportsWindow')