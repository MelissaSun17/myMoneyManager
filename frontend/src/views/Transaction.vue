<template>
  <section>
    <div class="row">
      <div class="col">
        <el-input placeholder="please enter here" prefix-icon="el-icon-search" v-model="searchFor" @change="search()">
        </el-input>
      </div>
      <div class="col">
        <base-button type="secondary" icon="ni ni-fat-add" @click="addTransaction=true">Add transaction</base-button>

      </div>
      <div class="col">
        <p v-if="groupOrNot!=='1'"> ID: {{ this.groupIdCurrent }}</p>
      </div>
    </div>
    <el-card class="box-card" style="margin: 20px;" v-if="groupOrNot!=='1'">
      <div slot="header" class="clearfix">
        <span>Group members</span>

        <base-button type="default" style="float: right" @click="deleteComfirm=true"> Delete Whole Group </base-button>
        <base-button type="secondary" style="float: right; margin-right: 10px;" @click="editGroup=true"> Edit and Add</base-button>
      </div>
      <div v-for="item in memberList" :key="item.userId" class="text item">
        {{item.email }}
      </div>
    </el-card>
    <el-table :data="table" style="width: 100%" empty-text="no data currently">
      <el-table-column prop="date" label="Date" width="180">
      </el-table-column>
      <el-table-column prop="category" label="Category" width="180">
      </el-table-column>
      <el-table-column prop="amount" label="Amount">
      </el-table-column>
      <el-table-column prop="description" label="Description">
      </el-table-column>
      <el-table-column label="Operation" width="120">
        <div slot-scope="scope">
          <i class="el-icon-edit" @click="editRow(scope.row)" style="margin-right: 10px;"></i>
          <i class="el-icon-delete" @click="deleteRow(scope.row)"></i>
        </div>
      </el-table-column>
    </el-table>
    <div class="row justify-content-center" style="margin-top: 20px;">
      <el-pagination ref="pagination" @current-change="handleCurrentChange" :current-page="currentPage" :page-size="pageSize" layout="total, prev, pager, next" :total="totalPage">
      </el-pagination>
    </div>

    <Modal :show.sync="addTransaction" body-classes="p-0" modal-classes="modal-dialog-centered modal-lg">
      <card type="secondary" shadow header-classes="bg-white pb-5" body-classes="px-lg-5 py-lg-5" class="border-0">
        <el-form ref="transactionInfo" :model="transactionInfo" label-width="100px">
          <el-form-item label="Date">
            {{ transactionInfo.date }}
          </el-form-item>
          <el-form-item label="Category">
            <el-select v-model="transactionInfo.category" placeholder="Please select the category">
              <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Amount">
            <el-input v-model="transactionInfo.amount"></el-input>
          </el-form-item>
          <el-form-item label="Description">
            <el-input v-model="transactionInfo.description"></el-input>
          </el-form-item>
          <span v-if="groupOrNot!=='1'">Note: This is a default shared transaction for all members in this group!! </span>
          <div class="text-center">
            <base-button type="default" class="my-4" @click="addTransactionNow()">Add the transaction</base-button>
            <base-button type="default" class="my-4" @click="cancel()">Cancel</base-button>
          </div>
        </el-form>
      </card>
    </Modal>
    <Modal :show.sync="editMode" body-classes="p-0" modal-classes="modal-dialog-centered modal-lg">
      <card type="secondary" shadow header-classes="bg-white pb-5" body-classes="px-lg-5 py-lg-5" class="border-0">
        <el-form ref="transactionInfo" :model="transactionInfo" label-width="100px">
          <el-form-item label="Date">
            {{ view.date }}
          </el-form-item>
          <el-form-item label="Category">
            <el-select v-model="view.category" placeholder="Please select the category">
              <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Amount">
            <el-input v-model="view.amount"></el-input>
          </el-form-item>
          <el-form-item label="Description">
            <el-input v-model="view.description"></el-input>
          </el-form-item>
          <div class="text-center">
            <base-button type="default" class="my-4" @click="finishEdit()">Save</base-button>
            <base-button type="default" class="my-4" @click="cancel()">Cancel</base-button>
          </div>
        </el-form>
      </card>
    </Modal>
    <Modal :show.sync="editGroup" body-classes="p-0" modal-classes="modal-dialog-centered modal-lg">
      <card type="secondary" shadow header-classes="bg-white pb-5" body-classes="px-lg-5 py-lg-5" class="border-0">
        <h3>All members here: </h3>
        <div v-for="(item, index) in memberList" :key="item.userId" class="text item" style="margin: 3%">
          {{item.email}}
          <base-button type="secondary" style="padding: 5px; margin-left: 15px;" @click="deleteGroupMember(item)"> Delete </base-button>
        </div>
        <el-form style="margin-bottom: 20px;">
          <el-form-item label="Invite new member: ">
            <el-input v-model="newMember"></el-input>
          </el-form-item>
          <base-button type="default" @click="addGroupMember()"> Add Group Member </base-button>
        </el-form>
      </card>
    </Modal>
    <modal :show.sync="deleteComfirm" gradient="default" modal-classes="modal-danger modal-dialog-centered">
      <h6 slot="header" class="modal-title" id="modal-title-notification">Your attention is required</h6>
      <div class="py-3 text-center">
        <i class="ni ni-bell-55 ni-3x"></i>
        <h4 class="heading mt-4">Do you want to delete the whole group? </h4>
        <!-- <p>A small river named Duden flows by their place and supplies it with the
                                                    necessary regelialia.</p> -->
      </div>
      <template slot="footer">
                                                <base-button type="white" @click="deleteWholeGroup()">Sure, please delete this group</base-button>
                                                <base-button type="link"
                                                             text-color="white"
                                                             class="ml-auto"
                                                             @click="deleteComfirm = false">
                                                    Close
                                                </base-button>
</template>
            </modal>
  </section>
</template>
<script>
  import Modal from "@/components/Modal.vue";
  import utils from "@/api/utils";
  export default {
    components: {
      Modal
    },
    props: {
      tableData: {
        type: Array,
        default: () => []
      },
      groupOrNot: {
        type: String,
        default: "1"
      },
      total: {
        type: Number,
        default: 0
      },
      groupId: {
        type: String,
        default: "0"
      }
    },
    data() {
      return {
        newMember: '',
        searchFor: '',
        addTransaction: false,
        transactionInfo: {
          date: this.currentDate(),
          category: '',
          amount: '',
          description: ''
        },
        groupIdCurrent: Number(this.groupId),
        table: this.tableData,
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
        value: '',
        editMode: false,
        view: {
          date: this.currentDate(),
          category: 0,
          amount: '',
          description: ''
        },
        currentPage: 1,
        pageSize: 10,
        totalPage: this.total,
        memberList: [],
        editGroup: false,
        deleteComfirm: false,
        userId: Number(window.sessionStorage.getItem('userId')),
        groupOrNotCurrent: this.groupOrNot
      }
    },
    mounted() {
      this.$emit("transaction-methods", this.callAllMethods);
    },
    methods: {
      callAllMethods() {
        if (this.groupOrNotCurrent !== '1') {
          this.getMemberList()
        }
        this.getTable()
      },
      findValue(label) {
        const option = this.options.find(option => option.label === label);
        if (option) {
          console.log(option.value); // Output the value (6 for 'transport')
          return option.value;
        }
        return null; // Return null if the label is not found in the options array
      },
      getLabelByValue(value) {
        const option = this.options.find(option => option.value === value);
        return option ? option.label : '';
      },
      handleCurrentChange(val) {
        this.currentPage = val
        this.getTable()
      },
      getSelfTransactions() {
        utils.getTransactionList({
          userId: this.userId,
          page: this.currentPage
        }).then((res) => {
          this.table = []
          console.log(res)
          this.totalPage = res.data.total_rows
          if (res.data.list.length !== 0) {
            this.totalPage = res.data.total_rows
            this.currentPage = res.data.current_page
            res.data.list.forEach((item) => {
              var arr = item.fields.createTime.split("T")
              this.table.push({
                date: arr[0],
                category: this.getLabelByValue(item.fields.category),
                amount: item.fields.values,
                description: item.fields.description,
                transactionId: item.pk,
                userId: item.ownerId
              })
            })
          }
        })
      },
      getGroupTransactions() {
        utils.getGroupTransactionListByGroupID({
          groupId: Number(this.groupIdCurrent),
          page: 1
        }).then((res) => {
          console.log(res)
          this.table = []
          this.totalPage = res.data.list.total_rows
          if (res.data.list.length !== 0) {
            this.totalPage = res.data.list.total_rows
            this.currentPage = res.data.list.current_page
            res.data.list.transactions.forEach((i) => {
              var arr = i.fields.createTime.split("T")
              this.table.push({
                date: arr[0],
                category: this.getLabelByValue(i.fields.category),
                amount: i.fields.values,
                description: i.fields.description,
                transactionId: i.pk,
                userId: this.userId
              })
            })
            console.log(this.table)
          }
        })
      },
      getMemberList() {
        utils.getMemberList({
          groupId: this.groupIdCurrent
        }).then((res) => {
          console.log(res)
          if (res.data.success) {
            let result = JSON.parse(res.data.result)
            this.memberList = result
          }
        })
      },
      getTable() {
        console.log(this.table)
        if (this.groupOrNotCurrent == "1") {
          this.getSelfTransactions()
        } else {
          this.getGroupTransactions()
        }
      },
      searchGroup(){
        utils.searchGroupTransaction({
          q: this.searchFor,
          groupId: this.groupIdCurrent
        }).then((res) => {
          console.log(res)
          if (res.data.list) {
            this.table = []
            this.totalPage = res.data.total_rows
            this.currentPage = res.data.current_page
            res.data.list.forEach((item) => {
              var arr = item.fields.createTime.split("T")
              this.table.push({
                date: arr[0],
                category: this.getLabelByValue(item.fields.category),
                amount: item.fields.values,
                description: item.fields.description,
                transactionId: item.pk,
                userId: item.ownerId
              })
            })
          }
        })
      },
      searchSelf(){
        utils.searchSelfTransaction({
          q: this.searchFor,
          userId: this.userId
        }).then((res) => {
          debugger
          console.log(res)
          if (res.data.list) {
            this.table = []
            this.totalPage = res.data.total_rows
            this.currentPage = res.data.current_page
            res.data.list.forEach((item) => {
              var arr = item.fields.createTime.split("T")
              this.table.push({
                date: arr[0],
                category: this.getLabelByValue(item.fields.category),
                amount: item.fields.values,
                description: item.fields.description,
                transactionId: item.pk,
                userId: item.ownerId
              })
            })
          }
        })
      },
      search() {
        console.log(this.searchFor)
        if (this.groupOrNotCurrent !== '1'){
          this.searchGroup()
        } else {
          this.searchSelf()
        }

      },
      editRow(row) {
        this.editMode = true;
        this.view = { ...row
        }
      },
      finishEdit() {
        let editVersion = this.view
        editVersion.values = Number(this.view.amount)
        editVersion.category = this.findValue(this.view.category)
        utils.editSelfTransaction(editVersion).then((res) => {
          debugger
          console.log(res)
          if (res.data.success) {
            this.getTable()
            this.$message({
              message: res.data.msg,
              type: 'success'
            })
          }
        })
        this.editMode = false;
      },
      deleteRow(row) {
        utils.deleteSelfTransaction({
          transactionId: row.transactionId
        }).then((res) => {
          console.log(res)
          debugger
          if (res.data.success) {
            this.getTable()
            this.$message({
              message: res.data.msg,
              type: 'success'
            })
          }
        })
      },
      addTransactionNow() {
        if (!this.table) {
          this.table = []
        }
        // ('category', 'description', 'values', 'ownerId')
        let transactionNow = {
          ownerId: this.userId,
          userId: this.userId,
          category: this.transactionInfo.category,
          description: this.transactionInfo.description,
          values: Number(this.transactionInfo.amount),
        }
        if (this.groupOrNotCurrent !== '1') {
          transactionNow.groupId = this.groupIdCurrent
          utils.addGroupTransaction(transactionNow).then((res) => {
            console.log(res)
            if (res.data == "Success") {
              this.getGroupTransactions()
              this.$message({
                message: 'successfully add!',
                type: 'success'
              })
            }
          })
        } else {
          utils.addSelfTransaction(transactionNow).then((res) => {
            console.log(res)
            if (res.data == "Success") {
              this.getSelfTransactions()
              this.$message({
                message: 'successfully add!',
                type: 'success'
              })
            }
          })
        }
        // this.table.push(this.transactionInfo)
        this.addTransaction = false
        this.transactionInfo = {
          date: this.currentDate(),
          category: '',
          amount: '',
          description: ''
        }
      },
      cancel() {
        this.addTransaction = false
        this.editMode = false
        this.transactionInfo = {
          date: this.currentDate(),
          category: '',
          amount: '',
          description: ''
        }
      },
      currentDate() {
        const current = new Date();
        const date = `${current.getFullYear()}-${current.getMonth()+1}-${current.getDate()}`;
        return date;
      },
      deleteGroupMember(item) {
        let deleteGroupMemberRes = {
          userId: this.userId,
          groupId: this.groupIdCurrent,
          email: item.email,
        }
        console.log(deleteGroupMemberRes)
        utils.removeGroupMember(deleteGroupMemberRes).then((res) => {
          console.log(res)
          debugger
          if (res.data.emailList) {
            this.$message({
              message: res.data.message,
              type: 'success'
            })
            this.getMemberList()
          }
        })
      },
      addGroupMember() {
        if (this.newMember && this.newMember !== '') {
          utils.addMember({
            userId: this.userId,
            groupId: this.groupIdCurrent,
            email: this.newMember
          }).then((res) => {
            if (res.data.emailList.length !== 0) {
              this.$message({
                message: res.data.message,
                type: 'success'
              })
              this.getMemberList()
            }
          })
          this.newMember = ''
        } else {
          this.$message('you cannot add an empty member')
        }
      },
      deleteWholeGroup() {
        this.deleteComfirm = false
        
        let deleteGroupMemberRes = {
          userId: this.userId,
          groupId: this.groupIdCurrent
        }
        utils.deleteGroup(deleteGroupMemberRes).then((res) => {
          console.log(res)
          debugger
          if (res.data.success) {
            this.$message({
              message: 'successfully delete!',
              type: 'success'
            })
            // this.$emit('remove-tab', "2");
            this.$emit('remove-tab', this.groupOrNot);
          }
        })
      },
      removeCurrentTab() {
        this.getSelfTransactions()
        this.$emit('remove-tab', this.groupOrNot);
      },
      updateTotalText() {
        this.$nextTick(() => {
          const elTotal = this.$refs.pagination.$el.querySelector('.el-pagination__total');
          if (elTotal) {
            elTotal.textContent = `Total: ${this.totalPage} items`;
          }
        });
      }
    }
  };
</script>
<style>

</style>
