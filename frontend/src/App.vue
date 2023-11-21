<template>
    <div class="app">
        <post-form @post_create="AddPost"/>
        <post-list :posts="posts"/>
    </div>
</template>

<script>
import PostForm from '@/components/PostForm';
import PostList from '@/components/PostList';
export default {
    components: {PostForm, PostList},
    data() {
        return {
            posts: [
                {id: 1, title: "osme title 1", created_at: "2022-05-05"},
                {id: 2, title: "osme title 2", created_at: "2022-05-06"},
                {id: 3, title: "osme title 3", created_at: "2022-05-07"},
            ],
        }
    },
    methods: {
        // Принимает аргументы переданные при генерации события в компоненте
        AddPost(post, message) {
            console.log(message);
            this.posts.push(post);
        }
    }
}
</script>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

.app {
    padding: 20px;
}

</style>