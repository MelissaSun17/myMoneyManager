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
                <base-button type="default" @click="addTabName=true">Add Group</base-button>
              </div>
              <el-tabs v-model="editableTabsValue" type="card" @tab-remove="removeTab" @tab-click="handleTabClick">
                <el-tab-pane v-for="(item, index) in editableTabs" :key="item.id" :label="item.title" :name="item.id">
                  <transaction :tableData="item.content" :groupId="item.id" :groupOrNot="item.name" :total="item.content.length" @remove-tab="removeTab" @transaction-methods="(methods) => registerMethods(item.id, methods)" ref="transactions">
                  </transaction>
                </el-tab-pane>
              </el-tabs>
            </card>
          </div>
        </div>
        <div class="col">
          <div style="margin: 5%">
            <card shadow>
              <div style="margin-bottom: 20px;">
                <base-button type="default" @click="generate()">Regenerate transaction visualisation</base-button>
              </div>
              <div id="chart">
                <apexchart type="treemap" height="350" :options="chartOptions" :series="series"></apexchart>
              </div>
            </card>
          </div>
        </div>
      </div>
    </div>
    <Modal :show.sync="addTabName" body-classes="p-0" modal-classes="modal-dialog-centered modal-sm">
      <card type="secondary" shadow header-classes="bg-white pb-5" body-classes="px-lg-5 py-lg-5" class="border-0">
        <form role="form">
          <base-input alternative class="mb-3" placeholder="Please enter here" addon-left-icon="ni ni-tag" v-model="newGroupName">
          </base-input>
          <div class="text-center">
            <base-button type="default" class="my-4" @click="addTab()">Create a new group</base-button>
          </div>
        </form>
      </card>
    </Modal>
  </div>
</template>


<script>
  import transaction from "./Transaction";
  import utils from "@/api/utils";
  import Modal from "@/components/Modal.vue";
  export default {
    components: {
      transaction,
      Modal
    },
    data() {
      return {
        baseUrl: '',
        jumpTo: true,
        activeName: 'Self-accounting',
        editableTabsValue: 'user',
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
        editableTabs: [{
            title: 'Self-accounting',
            name: '1',
            id: 'user',
            content: [],
            memberList: []
          }
        ],
        tabIndex: 2,
        addTabName: false,
        newGroupName: '',
        series: [{
          data: [{
            x: 'Please regenerate to view updated transactions',
            y: 1
          }]
        }],
        chartOptions: {
          legend: {
            show: false
          },
          chart: {
            height: 350,
            type: 'treemap'
          },
          title: {
            text: 'Transactions overview'
          }
        },
        userId: Number(window.sessionStorage.getItem('userId')),
        transactionMethods: {}
      };
    },
    mounted() {
      this.getGroupTransactions()
      this.$nextTick(() => {
        if (this.transactionMethods[this.editableTabsValue]) {
          this.transactionMethods[this.editableTabsValue]();
        }
      });
    },
    methods: {
      handleTabClick(tab) {
        this.$nextTick(() => {
          if (this.transactionMethods[tab.name]) {
            this.transactionMethods[tab.name]();
          }
        });
      },
      registerMethods(tabName, methods) {
        this.transactionMethods[tabName] = methods;
      },
      getLabelByValue(value) {
        const option = this.options.find(option => option.value === value);
        return option ? option.label : '';
      },
      getGroupTransactions() {
        utils.getGroupTransactionList({
          userId: this.userId,
          page: 1
        }).then((res) => {
          console.log(res)
          if (res.data.list.length !== 0) {
            res.data.list.forEach((item) => {
              let temp = {}
              temp.title = item.group_name
              temp.name = item.group_id
              temp.content = []
              temp.id = item.group_id
              // item.transactions.forEach((i) => {
              //   var arr = i.fields.createTime.split("T")
              //   temp.content.push({
              //     date: arr[0],
              //     category: i.fields.category,
              //     amount: i.fields.values,
              //     description: i.fields.description,
              //     transactionId: i.pk,
              //     userId: this.userId
              //   })
              // })
              this.editableTabs.push(temp)
            })
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
      generate() {
        utils.getSummary({
          userId: this.userId
        }).then((res) => {
          debugger
          console.log(res)
          var newData = []
          if (res.data.success) {
            res.data.result.detail.forEach((item) => {
              debugger
              newData.push({
                x: this.getLabelByValue(item.category),
                y: Number(item.value)
              })
            })
            this.series = [{
              data: newData
            }]
          }
        })
      },
      addTab() {
        let newTabName = "group";
        utils.createGroup({
          name: this.newGroupName,
          userId: this.userId
        }).then((res) => {
          debugger
          console.log(res)
          if (res.data.groupId) {
            this.$message({
              message: 'successfully add the group!',
              type: 'success'
            })
            this.editableTabs.push({
              title: this.newGroupName,
              name: newTabName,
              id: res.data.groupId,
              content: [],
              memberList: []
            });
            // this.editableTabsValue = res.data.groupId;
          }
        })
        // this.editableTabsValue = newTabName;
        this.addTabName = false;
      },
      removeTab(targetName) {
        let tabs = this.editableTabs;
        let activeName = this.editableTabsValue;
        if (activeName === targetName) {
          tabs.forEach((tab, index) => {
            if (tab.name === targetName) {
              let nextTab = tabs[index + 1] || tabs[index - 1];
              if (nextTab) {
                activeName = nextTab.name;
              }
            }
          });
        }
        // this.editableTabsValue = activeName;
        this.editableTabs = tabs.filter(tab => tab.name !== targetName);
        this.editableTabsValue = this.editableTabs[0].id;
      }
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
