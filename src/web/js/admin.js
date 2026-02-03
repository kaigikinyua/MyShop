

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

//*********Sales Components*************/
const sales_reports={
    template:`
    <div class="topNav" id="sales_reports">
        <div>
            <h3> {{ currentTab }} </h3>
        </div>
    </div>
    <div class="appView">
        <div>
            Get report for date <input class="dateField" type="date" placeholder="Pick a day"/>
        </div>
        <div>
            <h4>X Report</h4>
            <div>X Report Content</div>
        </div>
        <div>
            <h4>Z Report</h4>
            <div>Z Report Content</div>
        </div>
        <div>
            <h4>Stock Report</h4>
            <div>Stock Report Content</div>
        </div>
        <div>
            <h4>Credit Report</h4>
            <div>Credit Report Content</div>
        </div>
    </div>
    `,
    data(){
        return {
            currentTab:'Sales Reports'
        }
    }
}
const sales_analysis={
    template:`
        <div class="topNav" id="sales_analysis">
        <div>
            <h3> {{ currentTab }} </h3>
        </div>
        </div>
        <div class="appView">
            <div class='inline'>
                <span>
                    From: <input class="dateField" type="date" name="startDate"/>
                </span>
                <span>
                    To:<input class="dateField" type="date" name="endDate"/>
                </span>
            </div>
            <div>

            </div>
        </div>
    `,
    data(){
        return {
            currentTab:'Sales Analysis'
        }
    }
}
const sales_targets={
    template:`
        <div class="topNav" id="sales_targets">
        <div>
            <h3> {{ currentTab }} </h3>
        </div>
        </div>
        <div class="appView">
            <div class='inline'>
                <span>
                    From: <input class="dateField" type="date" name="startDate"/>
                </span>
                <span>
                    To:<input class="dateField" type="date" name="endDate"/>
                </span>
            </div>
        
        </div>
    `,
    data(){
        return {
            currentTab:'Sales Targets',
            id:'testId'
        }
    }
}

//*********Stock Components****************/


//*********Main App***********************/
const appView={
    template:`
    <sales_reports></sales_reports>
    <sales_analysis></sales_analysis>
    <sales_targets></sales_targets>    
    `,
    components:{
        sales_reports,
        sales_analysis,
        sales_targets
    },
    data(){
        return{
            currentTab:'sales_reports',
            tabs:['sales_reports','sales_analysis','sales_targets']
        }
    },
    methods:{
        changeComponent(componentName){
            console.log('changing tab')
            this.currentTab=componentName
        }
    }

}


const app=Vue.createApp({})
app.component('app-view',appView)
app.mount('#mainAppView')