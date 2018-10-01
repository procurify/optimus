<template>
    <ul>
        <li v-for="(value, key) in schema">
            <a href="#" v-on:click="highlight(value['id'])">
                {{ key }}: {{ value['source'] }} ({{ value['type'] }})
            </a>

            <node :schema="value['items']['properties']" v-if="value['type'] === 'array'"></node>

            <node :schema="value['properties']" v-if="value['type'] === 'object'"></node>
        </li>
    </ul>
</template>

<script>
    import {find} from 'lodash'

    export default {
        name: "node",

        props: {
            schema: Object,
            required: true
        },

        methods: {
            highlight: function (id) {
                const result = find(this.schema, {id: id})
                result.type = "number"
            }
        }

    }
</script>

<style scoped>

</style>
