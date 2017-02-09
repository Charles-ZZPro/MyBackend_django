<template>
  <div id="mask"></div>
</template>
<script>
  export default {
    mounted() {

      this.$el.style.height = document.body.scrollHeight || 1000+ 'px';

    }
  }
</script>
<style scoped>
  #mask {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: #fff;
    opacity: 1;
    z-index: 100;
  }
</style>
