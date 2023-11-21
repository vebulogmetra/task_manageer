<template>
    <h3>Posts list</h3>
    <div>
        <post-item :post="post" v-for="post in posts"/>
    </div>
</template>

<script>
import PostItem from "@/components/PostItem"
export default {
    components: {PostItem},
    props: {
        posts: {
            type: Array,
            required: true
        }
    }
}
</script>

<style scoped>

</style>