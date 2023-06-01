<template>
  <div class="overall">
    <section class="section-shaped my-0" style="height: 300px;">
    </section>
    <div class="ct-example-row">
      <div class="row">
        <div class="col">
          <div style="margin: 5%">
            <card shadow>
              <div style="margin-bottom: 20px;">
              </div>
              <base-input alternative class="mb-3" style="max-width: 500px;" 
              placeholder="Please enter the group id here" addon-left-icon="el-icon-search" 
              v-model="groupId"
              @change="getGroupTransactions()">
              </base-input>
              <base-button type="default" @click="getGroupTransactions()"> Search </base-button>
              <el-table :data="tableList" style="width: 100%" empty-text="no data currently">
                    <el-table-column prop="date" label="Date" width="180">
                    </el-table-column>
                    <el-table-column prop="category" label="Category" width="180">
                    </el-table-column>
                    <el-table-column prop="amount" label="Amount">
                    </el-table-column>
                    <el-table-column prop="description" label="Description">
                    </el-table-column>
                  </el-table>
            </card>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>


<script>
  import transaction from "./Transaction";
  import utils from "@/api/utils";
  export default {
    components: {
      transaction
    },
    data() {
      return {
        options: [{
          value: 1,
          label: 'groceries'
        }, {
          value: 2,
          label: 'charity'
        }, {
          value: 3,
          label: 'restaurant'
        }, {
          value: 4,
          label: 'entertainment'
        }, {
          value: 5,
          label: 'general'
        }, {
          value: 6,
          label: 'transport'
        }, {
          value: 7,
          label: 'other'
        }],
        groupId: '',
        jumpTo: true,
        editableTabs: {
          title: 'visitor mode',
          name: "1",
          memberList: [],
          content: []
        },
        tableList: [],
        totalPage: 0,
        currentPage: 1
      };
    },
    mounted() {},
    methods: {
      getLabelByValue(value) {
        const option = this.options.find(option => option.value === value);
        return option ? option.label : '';
      },
      getGroupTransactions() {
        utils.getGroupTransactionListByGroupID({
          groupId: Number(this.groupId),
          page: 1
        }).then((res) => {
          console.log(res)
          this.tableList = []
          debugger
          if (res.data.list.length !== 0) {
            res.data.list.transactions.forEach((i) => {
              var arr = i.fields.createTime.split("T")
              this.tableList.push({
                date: arr[0],
                category: this.getLabelByValue(i.fields.category),
                amount: i.fields.values,
                description: i.fields.description,
                transactionId: i.pk,
                userId: this.userId
              })
            })
            console.log(this.tableList)
          }
        })
      },
      jumpToProfile() {
        if (this.jumpTo) {
          this.$router.push({
            path: 'profile'
          })
        }
      },
    }
  };
</script>
<style scoped>
  .overall {
    background-image: url('../assets/img/accountingBackground.jpg');
    padding-bottom: 600px;
    margin-bottom: 5%;
  }
</style>
