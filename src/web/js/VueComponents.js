const productsComponent = {
  template: `
    <div>
      <h2>Products Component</h2>
      <table>
        <tr>
            <th>Item Name</th>
            <th>Bar Code</th>
            <th>Price</th>
        </tr>
        <tr v-for="item in items">
            <td>{{item.name}}</td>
            <td>{{item.barCode}}</td>
            <td>{{item.sPrice}}</td>
        </tr>
      </table>
    </div>
  `,
  data(){
    return {
        items:[],
        isLoading:true,
        error:null
    }
  },
  async mounted(){
        var response= await eel.getProductsAndBranches()()
        if(response!=null){
            this.items=response['products']
        }
    }
};

const transactionsComponent={
    template:`
        <div>
            <h2>Transactions Component</h2>
            <table>
                <tbody>
                <tr>
                    <th>Transaction Id</th>
                    <th>Customer Id</th>
                    <th>Customer Name</th>
                    <th>Sale Amount</th>
                    <th>Paid Amount</th>
                    <th>Sell Date</th>
                </tr>
                <tr v-for='t in transactions'>
                    <td>{{t.id}}</td>
                    <td>{{t.custId}}</td>
                    <td>{{t.customerDetails['name']}}</td>
                    <td>{{t.saleAmount}}</td>
                    <td>{{t.paidAmount}}</td>
                    <td>{{t.sellDate}}</td>
                <tr>
                </tbody>
            </table>
        </div>
    `,
    data(){
        return {
            transactions:[],
            isLoading:true,
            error:null
        }
    },
    async mounted(){
        var response=await eel.getAllTransactions()()
        this.transactions=response['transactions']
    }
};



const app=Vue.createApp({})
app.component('products-component',productsComponent)
app.component('transactions-component',transactionsComponent)
app.mount('#app')

