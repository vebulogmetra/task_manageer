<template>
<button class="btn">
    <slot></slot>
</button>
</template>

<script>
export default {
    name: 'root-button'
}
</script>

<style scoped>
.btn {
    padding: 10px 15px;
    background: none;
    color: #757575;
    margin-top: 15px;
    border: 2px solid #177e64;
}
</style>