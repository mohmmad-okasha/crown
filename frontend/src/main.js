import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import axios from "axios";
import swal from 'sweetalert';
import VueI18n from 'vue-i18n'

axios.defaults.baseURL ='http://127.0.0.1:8000';

Vue.use(VueI18n)



const i18n = new VueI18n({
  locale: 'en',
  messages: {
    'ar': {

      //errors
      'Please Enter The Name': 'يرجى ادخال الاسم',
      'Please Select Type': 'يرجى تحديد النوع',
      'Please Enter Mobile Number': 'يرجى ادخال رقم الهاتف ',
      'Please Select ID Type': 'يرجى تحديد نوع الوثيقة',
      'Please Enter ID Number': 'يرجى ادخال رقم الوثيقة',
      'Please Enter The Address': 'يرجى ادخال العنوان',

      //settings
      'Language':'اللغة',
      'Arabic':'عربي',
      'English':'انجليزي',
      'On':'مفعل',
      'Off':'مغلق',
      'Dark Mode':'الوضع المظلم',


      'User': 'المستخدم',
      'Profile': 'الحساب',
      'Login': 'تسجيل الدخول',
      'Logout': 'تسجيل الخروج',
      'Activity Log': 'سجل الحركات',
      'Settings': 'الاعدادات',
      'Users': 'المستخدمين',
      'Customer': 'عميل',
      'Supplier': 'مورد',
      'Customers': 'العملاء',
      'Persons': 'الأشخاص',
      'Employees': 'الموظفين',
      'Table': 'جدول',
      'Customers Table': 'جدول العملاء',
      'Search for...': '...البحث عن',
      'Alerts Center': 'الاشعارات',
      'Show All Alerts': 'عرض جميع الاشعارات',
      'Message Center': 'الرسائل',
      'Read More Messages': 'عرض جميع الرسائل',
      'Dashboard': 'لوحة التحكم',
      'Name': 'الاسم',
      'Mobile': 'الهاتف',
      'Type': 'النوع',
      'ID Type': 'الوثيقة',
      'ID Number': 'رقم الوثيقة',
      'Address': 'العنوان',
      'Notes': 'الملاحظات',
      'Image': 'الصورة',
      'Actions': 'الخيارات',
      'Delete': 'حذف',
      'Edit': 'تعديل',
      'Save': 'حفظ',
      'Close': 'اغلاق',
      'Cancel': 'الغاء',
      'Print': 'طباعة',
      'Add': 'اضافة',
      'add': 'اضافة',
      'new': 'اضافة',
      'New': 'اضافة',
      'Updated': 'تم التحديث',
      'Saved': 'تم الحفظ',
      'Number': 'رقم',
      'Number of': 'رقم',
      'Residence': 'إقامة',
      'Driving License': 'رخصة قيادة',
      'Passport': 'جواز سفر',
      'ID Card': 'بطاقة هوية',
      'Choose Picture': 'اختر صورة',
      'Add Customer': 'اضافة عميل',
      'Edit Customer': 'تعديل عميل',

      'Are you sure?': 'هل انت متأكد؟',
      'Deleted!': 'تم الحذف',
      'Updated!': 'تم التحديث',
      'Added!': 'تمت الاضافة',

    }
  }
});


Vue.config.productionTip = false;



new Vue({
  i18n,
  router,
  store,
  axios,
  swal,
  render: (h) => h(App),
}).$mount("#app");
