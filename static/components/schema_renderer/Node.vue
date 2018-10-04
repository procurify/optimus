<template>
    <ul>
        <li v-for="(value, key) in schema">
            <a v-on:click.stop="selectionHandler(value['id'])">
                {{ key }}: {{ value['source'] }}
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
    a {
        cursor: pointer;
    }
</style>
