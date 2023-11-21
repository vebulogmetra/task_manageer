<template>
        <form @submit.prevent>
        <h3>Create post</h3>
        <input v-model="post.title" class="input" type="text" placeholder="title">
        <input v-model="post.created_at" class="input" type="text" placeholder="date">
        <root-button class="create-btn" @click="AddPost">Create</root-button>
        </form>
</template>

<script>
export default {
    data() {
        return {
            post: {
                title: '',
                created_at: new Date().toJSON().slice(0,10)
            }
        }
    },
    methods: {
        AddPost() {
            this.post.id = Date.now(),
            // Компонент не может изменять пропсы, поэтому они должны меняться в родителе
            // Это делается с помощью генерации события, на которое подписан родитель
            this.$emit("post_create", this.post, "Its work!")
            // Очищаем инпуты
            this.post = {
                title: '',
                created_at: new Date().toJSON().slice(0,10)
            }
        }
    }
}
</script>

<style scoped>
form {
    display: flex;
    flex-direction: column;
}

.input {
    width: 100%;
    border: 2px solid #6fccb5;
    padding: 10px 15px;
    margin-top: 15px;
}

.create-btn {
    align-self: flex-end;
}
</style>