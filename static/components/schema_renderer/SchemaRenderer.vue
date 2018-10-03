<template>
    <div class="tree">
        <object-form :instance="instance"
                     v-if="instance != null"
                     @close="saveInstance"></object-form>

        <node :schema="local_schema.properties"
              :selectionHandler="selectInstance"
              v-if="local_schema !== null"></node>
    </div>
</template>

<script>

    import {find, cloneDeep} from 'lodash'
    import Node from './Node.vue'
    import ObjectForm from './ObjectForm.vue'


    const findObjectByID = function (schema, id) {
        let result = null
        const keys = Object.keys(schema)

        for (let i = 0; i < keys.length; i++) {
            const key = keys[i]
            const value = schema[key]

            if (value.id === id) {
                result = value
            }

            if (result !== null) break

            if (value.type === "object") {
                result = findObjectByID(value.properties, id)
            } else if (value.type === "array") {
                result = findObjectByID(value.items.properties, id)
            }

        }

        return result
    }

    export default {
        name: 'schema-renderer',

        props: {
            schema: Object,
        },

        data: function () {
            return {
                instance: null,
                local_schema: null
            }
        },

        methods: {
            selectInstance: function (id) {
                this.instance = findObjectByID(this.local_schema.properties, id)
            },
            saveInstance: function () {
                this.instance = null
                this.$emit('update:schema', this.local_schema)
            }
        },

        watch: {
            schema: function (new_value, old_value) {
                this.local_schema = cloneDeep(new_value)

            }
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
