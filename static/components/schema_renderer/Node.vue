<template>
    <ul>
        <li v-for="(value, key) in schema">
            <a href="#" v-on:click="selectionHandler(value['id'])">
                {{ key }}: {{ value['source'] }} ({{ value['type'] }})
            </a>

            <node :schema="value['items']['properties']"
                  :selectionHandler="selectionHandler"
                  v-if="value['type'] === 'array'"></node>

            <node :schema="value['properties']"
                  :selectionHandler="selectionHandler"
                  v-if="value['type'] === 'object'"></node>
        </li>
    </ul>
</template>

<script>
    export default {
        name: "node",

        props: {
            schema: Object,
            selectionHandler: Function
        }
    }
</script>

<style scoped>

</style>
