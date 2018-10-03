<template>
    <div class="tree">
        <object-form :instance="instance"
                     v-if="instance != null"
                     @close="saveInstance"></object-form>

        <node :schema="schema.properties"
              :selectionHandler="selectInstance"
              v-if="schema !== null"></node>
    </div>
</template>

<script>

    import {find} from 'lodash'
    import Node from './Node.vue'
    import ObjectForm from './ObjectForm.vue'

    const data = {
        instance: null,

    }

    const findObjectByID = function (schema, id) {
        const keys = Object.keys(schema)

        for (let i = 0; i < keys.length; i++) {
            const key = keys[i]
            const value = schema[key]

            if (value.type === "object") {
                return findObjectByID(value.properties, id)
            } else if (value.type === "array") {
                return findObjectByID(value.items.properties, id)
            } else {
                if (value.id === id) {
                    return value
                }
            }

        }

        return null
    }

    export default {
        name: 'schema-renderer',

        props: {
            schema: Object,
            schema_edited: Function
        },

        data: function () {
            return data
        },

        methods: {
            selectInstance: function (id) {
                data.instance = findObjectByID(this.schema.properties, id)
            },
            saveInstance: function () {
                data.instance = null
                this.$emit('schema_edited', this.schema)
            }
        },

        watch: {
            // schema: function (new_value) {
            //     data.rendered_schema = {schema: new_value}
            // }
        },

        components: {
            Node,
            ObjectForm
        }
    }
</script>

<style scoped>
    .tree-list ul {
        padding-left: 16px;
        margin: 6px 0;
    }
</style>
