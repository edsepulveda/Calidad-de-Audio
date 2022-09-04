<template>


  <div class="container mt-2 p-2 d-flex justify-content-center animate__animated animate__fadeInDown">
    <img class="p-2" src="@/assets/logoA.png"/>
    <div class="mt-5">
      <h1>Servicios de Audio</h1>
    </div>
  </div>

  <div  class="container d-flex justify-content-center  animate__animated animate__fadeIn">
    <div id="fileUpload" class="card p-3 shadow-sm border">
        <input type="file" id="file" ref="file" @change="handleFileUpload($event)"/>
    </div>
  </div>

  <div class="container d-flex justify-content-center  animate__animated animate__fadeInLeft">
    
    <div id="calidad" class="col-4-sm p-3 border mt-4">

      <h5 class="p-2"><b>Reglas de Calidad</b></h5>

      <table class="table table-borderless ">
        <tr>
          <th class="text-left" scope="col">FILTRO</th>
          <th scope="col">RESULTADO</th>
        </tr>

        <tr>
          <th class="text-left" scope="col">Silencio Total</th>
          <th scope="col"><label v-if="silencioTotal">{{ silencioTotal }} segundos</label></th>
        </tr>

        <tr>
          <th class="text-left" scope="col">Silencio al Final</th>
          <th scope="col"><label v-if="silencioFinal">{{ silencioFinal }} segundos</label></th>
        </tr>
        
        <tr>
          <th class="text-left" scope="col">Tiempo de Espera</th>
          <th scope="col"><label v-if="tiempoEspera">{{ tiempoEspera }} segundos</label></th>
        </tr>
        
      </table>

      <template v-if="audioCargado">
          <button @click="submitFile" id="calc"  class="btn btn-success mr-4" >Calcular</button>
          <button @click="reset" id="reset" class="btn btn-info" disabled>Reset</button>
      </template>

    </div>
    
  </div>

</template>



<script>

import silenceApi from '../api/silenceApi'
import Swal from 'sweetalert2'

  export default {

    data(){

      return {
        file: '',
        audioCargado: false,
        silencioFinal: null,
        silencioTotal: null,
        tiempoEspera: null,

      }
    },
    methods: {

      submitFile() {

        const btnCalc = document.getElementById('calc')
        const btnReset = document.getElementById('reset')
        const fileInput = document.getElementById('file')
        
        console.log(' se llamo el submit file')

        let formData = new FormData();
        formData.append('files', this.file);

        silenceApi.post('/silence',formData)
        .then( ( { data } ) => {
          
          if( data.msg ) {
            Swal.fire({
              icon: 'error',
              title: 'Error al calcular',
              text: data.msg,
            })
            this.reset()
          }
          else {
            btnCalc.disabled = true
            btnReset.disabled = false
            fileInput.disabled = true

            this.tiempoEspera  =  data.initial_silence
            this.silencioTotal =  data.total_silence
            this.silencioFinal =  data.final_silence
          }

        })
        .catch( ( e ) => console.log( e, 'ERROR') )
      },


      handleFileUpload(){
        this.file = this.$refs.file.files[0] 
        this.audioCargado = true
        console.log('Se llamo handleupload')
      },

      reset() {
        const file = document.getElementById('file')
        file.value= ''
        this.tiempoEspera  = null
        this.silencioFinal = null
        this.silencioTotal = null
        this.audioCargado  = null
        file.disabled = false

      }
    },

  }
</script>





<style scoped>

.animate__fadeInDown {
  animation-duration: 2.2s;
}

.animate__fadeInLeft {
  animation-duration: 2.2s;
}

.animate__fadeIn {
  animation-duration: 5s;
}

#calidad{
  background-color: #f1faee;
}

#fileUpload{
  background-color: #f1faee;
}


</style>
 