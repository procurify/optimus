<template>
    <ul>
        <li v-for="(value, key, index) in schema">
            <a v-on:click.stop="selectionHandler(value['id'], 'EDIT')">
                {{ key }}: {{ value['source'] }}
            </a> <a v-on:click.stop="selectionHandler(value['id'], 'DELETE')">&times;</a>

            <node :schema="value['items']['properties']"
                  :selectionHandler="selectionHandler"
                  v-if="value['type'] === 'array'"></node>

            <node :schema="value['properties']"
                  :selectionHandler="selectionHandler"
                  v-if="value['type'] === 'object'"></node>

            <div v-if="index === Object.keys(schema).length - 1">
                <button v-on:click="selectionHandler(value['id'], 'CREATE')">
                    &plus;
                </button>
            </div>
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
