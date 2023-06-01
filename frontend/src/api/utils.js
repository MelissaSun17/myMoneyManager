import request from "./request"

export default {

  register(data) {
    return request.postJson('/myMoneyManager/user_register/', data);
  },

  login(data) {
    return request.postJson('/myMoneyManager/user_login/', data);
  },

  getTransactionList(data) {
    return request.getJson(`/myMoneyManager/transaction/?userId=${data.userId}&page=${data.page}`)
  },

  addSelfTransaction(data) {
    return request.postJson('/myMoneyManager/add_transaction/', data);
  },

  editSelfTransaction(data) {
    return request.postJson('/myMoneyManager/edit_transaction/', data);
  },


  deleteSelfTransaction(data) {
    return request.postJson('/myMoneyManager/delete_transaction/', data);
  },

  searchSelfTransaction(data) {
    return request.getJson(`/myMoneyManager/search_transaction/?userId=${data.userId}&q=${data.q}`);
  },

  createGroup(data){
    return request.postJson('/myMoneyManager/create_group/', data);
  }, 

  addMember(data){
    return request.postJson('/myMoneyManager/add_member/', data);
  }, 

  deleteGroup(data){
    return request.postJson('/myMoneyManager/delete_group/', data);
  }, 

  removeGroupMember(data){
    return request.postJson('/myMoneyManager/remove_member/', data);
  }, 

  getGroupTransactionList(data){
    return request.getJson(`/myMoneyManager/transaction_group/?userId=${data.userId}&page=${data.page}`);
  }, 

  getGroupTransactionListByGroupID(data){
    return request.getJson(`/myMoneyManager/transaction_group/?groupId=${data.groupId}&page=${data.page}`);
  }, 

  searchGroupTransaction(data){
    return request.getJson(`/myMoneyManager/search_transaction_group/?groupId=${data.groupId}&q=${data.q}`);
  },

  getSummary(data){
    return request.postJson('/myMoneyManager/get_summary/',data);
  }, 

  setBudget(data){
    return request.postJson('/myMoneyManager/set_budget/',data);
  }, 

  addGroupTransaction(data){
    return request.postJson('/myMoneyManager/add_transaction_group/', data);
  },

  getMemberList(data){
    return request.postJson('/myMoneyManager/get_members_by_group_id/', data);
  },

  

  logout(data){
    return request.postJson('/myMoneyManager/user_logout/', data)
  }


  // path('search_transaction_group/', views.search_transactions_group, name='search_transactions_group'),

  // path('user_logout/', views.user_logout, name='user_logout'),


};

