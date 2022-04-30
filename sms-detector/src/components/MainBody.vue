<template>
  <v-container>
    <div class="mx-auto" style="width: 60%">
      <div class="mt-12">
        <v-form
          ref="form"
          v-model="valid"
          lazy-validation
          @submit.prevent="check"
        >        
          <v-textarea
            outlined
            auto-grow
            name="input"
            label="Enter Your SMS Here"
            v-model="input_content"
            :rules="[v => /\S/.test(v) || 'Item is required']" 
          >
          <!-- rules 只要有一个非空字符即合法 -->
          </v-textarea>
          <div class="d-flex" style="align-items: center; justify-content: flex-end; flex-wrap: wrap">
            <v-chip-group
              v-model="selectedClf"
              active-class="primary--text"
              class="my-6"
            >
              <v-chip
                v-for="clf in classifiers"
                :key="clf"
                :value="clf"
              >
                {{clf}}
              </v-chip>
            </v-chip-group>
            <span style="flex-grow: 1"></span>
            <v-btn depressed color="warning" @click="reset"> RESET </v-btn>
            <v-btn depressed color="primary" :disabled="!valid || loading" :loading="loading" class="ml-8" type="submit"> CHECK </v-btn>
          </div>
        </v-form>
      </div>
      <v-data-table
        :headers="headers"
        :items="sms"
        class="elevation-1 mt-12"
        hide-default-footer
        disable-pagination
      >
        <template v-slot:[`item.result`]="{ item }">
          <v-chip
            :color="getColor(item.result)"
            dark
          >
            {{ item.result }}
          </v-chip>
        </template>
      </v-data-table>    
    </div>
  </v-container>
</template>

<script>
export default {
  name: "MainBody",

  data: () => ({
    input_content: [
      'WINNER!! As a valued network customer you have been selected to receivea å£900 prize reward! To claim call 09061701461. Claim code KL341. Valid 12 hours only.',
      'I HAVE A DATE ON SUNDAY WITH WILL!!',
      'XXXMobileMovieClub: To use your credit, click the WAP link in the next txt message or click here>> http://wap. xxxmobilemovieclub.com?n=QJKGIGHJJGCBL',
      "I've been searching for the right words to thank you for this breather. I promise i wont take your help for granted and will fulfil my promise. You have been wonderful and a blessing at all times.",
      'For fear of fainting with the of all that housework you just did? Quick have a cuppa',
    ].join('\n'),
    headers: [
          {
            text: 'SMS', 
            value: 'content', 
            sortable: false,
          },
          { 
            text: 'Result', 
            value: 'result', 
            sortable: false,
            width: "4em",
          },
        ],
    sms: [
      {
        content: 'WINNER!! As a valued network customer you have been selected to receivea å£900 prize reward! To claim call 09061701461. Claim code KL341. Valid 12 hours only.',
        result: 'spam'
      },
      {
        content: 'I HAVE A DATE ON SUNDAY WITH WILL!!',
        result: 'ham'
      },
      {
        content: 'XXXMobileMovieClub: To use your credit, click the WAP link in the next txt message or click here>> http://wap. xxxmobilemovieclub.com?n=QJKGIGHJJGCBL',
        result: 'spam'
      },
      {
        content: "I've been searching for the right words to thank you for this breather. I promise i wont take your help for granted and will fulfil my promise. You have been wonderful and a blessing at all times.",
        result: 'ham'
      },
      {
        content: 'For fear of fainting with the of all that housework you just did? Quick have a cuppa',
        result: 'ham'
      },
    ],
    valid: false,
    loading: false,
    classifiers: [
      "GaussianNB",
      "SVC",
      "LinearSVC",
      "LogisticRegression",
      "SGDClassifier",
      "KNeighborsClassifier",
      "MLPClassifier",
    ],
    selectedClf: ""
  }),
  methods: {
    getColor (result) {
      if (result === 'ham') return 'green'
      else return 'red'
    },
    check (){

      if(this.$refs.form.validate()){
        this.loading = true
        fetch(`${window.location.href}predict`, {
          method: "POST",   
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
          },
          body: new URLSearchParams({sms_req: this.input_content, selectedClf: this.selectedClf?this.selectedClf:""})
        })
        .then(response => response.json())
        .then(result => {
          console.log('Success:', result);
          this.sms = result
        this.loading = false
        })        
      }
    },
    reset (){
      this.input_content = ""
    }
  }
};
</script>
