<template>
    <div>
        <tree :schema="schema"></tree>
    </div>
</template>

<script>
    import {debounce} from 'lodash'
    import Tree from './Tree.vue'

    const data = {
        rendered_schema: null,
    }

    export default {

        props: {
            schema: Object
        },

        components: {
            Tree
        },

        data: function () {
            return data
        }
    }

</script>

<style scoped>

</style>
