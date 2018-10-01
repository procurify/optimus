<template>
    <div class="tree">
        <ul class="tree-list">
            <li v-for="(value, key) in rendered_schema">
                {{ key }}:
                <node :schema="value['properties']" v-if="isObject(value)"></node>
            </li>

        </ul>
    </div>
</template>

<script>

    import Node from './Node.vue'

    const data = {
        rendered_schema: null
    }

    export default {
        name: 'tree',

        props: {
            schema: Object
        },

        data: function () {
            return data
        },

        methods: {
            isObject: function (value) {
                return value['type'] === 'object'
            }
        },

        watch: {
            schema: function (new_value) {
                data.rendered_schema = {schema: new_value}
            }
        },
        
        components: {
            Node
        }
    }
</script>

<style scoped>
    .tree-list ul {
        padding-left: 16px;
        margin: 6px 0;
    }
</style>
