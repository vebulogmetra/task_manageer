<template>
    <div class="post">
        <div>post id: <strong>{{ post.id }}</strong></div>
        <div>post title: <strong>{{ post.title }}</strong></div>
        <div>post created_at: <strong>{{ post.created_at }}</strong></div>
    </div>
    <div class="post__btns">
        <root-button>Delete</root-button>
    </div>
</template>

<script>
export default {
    props: {
        post: {
            type: Object,
            required: true
        }
    }
}

</script>

<style scoped>
.post {
    padding: 15px;
    border: 2px solid #177e64;
    margin-top: 15px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

</style>