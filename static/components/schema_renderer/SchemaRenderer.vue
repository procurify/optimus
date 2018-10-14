<template>
    <div class="tree">
        <object-form :instance="instance"
                     v-if="instance != null"
                     @close="saveInstance"></object-form>

        <node :schema="schema.properties"
              :selectionHandler="selectInstance"
              v-if="schema !== null"></node>

        <button v-on:click="printSchema">&#128424;</button>
    </div>
</template>

<script>

    import {cloneDeep, omit} from 'lodash'
    import Node from './Node.vue'
    import ObjectForm from './ObjectForm.vue'
    import {
        schemaGenerator,
        findObjectByID,
        redrawSchema,
        deleteObjectByID,
        createObjectByID
    } from '../../utils'


    const data = {
        instance: null,
        schema: null
    }

    export default {
        name: 'schema-renderer',

        props: {
            source: Object,
        },

        data: function () {
            return data
        },

        methods: {
            selectInstance: function (id, action) {
                switch (action) {
                    case 'CREATE':
                        data.instance = createObjectByID(data.schema, id)
                        break
                    case 'EDIT':
                        data.instance = findObjectByID(data.schema.properties, id)
                        break
                    case 'DELETE':
                        const local_schema = cloneDeep(data.schema)
                        local_schema.properties = deleteObjectByID(local_schema.properties, id)
                        data.schema = local_schema
                        this.$emit('schema_generated', data.schema)
                        break
                    default:
                        // Nothing
                }

            },
            saveInstance: function () {
                data.instance = null
                const local_schema = cloneDeep(data.schema)
                local_schema.properties = redrawSchema(local_schema.properties)
                data.schema = local_schema
                this.$emit('schema_generated', data.schema)
            },
            printSchema: function () {
                console.log(JSON.parse(JSON.stringify(this.schema)))
            }
        },

        watch: {
            source: function (new_value, old_value) {
                data.schema = schemaGenerator(new_value)
                this.$emit('schema_generated', data.schema)
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
