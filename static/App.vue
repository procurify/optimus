<template>
    <div class="full-width">
        <h1>Optimus</h1>

        <div class="container">
            <div class="column">
                <file-upload v-on:file_uploaded="onFileUploaded"></file-upload>
            </div>
            <div class="column">
                <schema-renderer :source="source" v-on:schema_generated="onSchemaGenerated"></schema-renderer>
            </div>
            <div class="column">
                <transformer :source="source" :schema="schema"></transformer>
            </div>
        </div>
    </div>
</template>

<script>
    import FileUpload from './components/FileUpload.vue'
    import SchemaRenderer from './components/schema_renderer/SchemaRenderer.vue'
    import Transformer from './components/Transformer.vue'

    const data = {
        source: null,
        schema: null,
        name: null,
        transformed: null
    }

    export default {
        components: {
            FileUpload,
            SchemaRenderer,
            Transformer,
        },

        data: function () {
            return data
        },

        methods: {
            onFileUploaded (source) {
                data.source = source
            },

            onSchemaGenerated (schema) {
                data.schema = schema
            }
        }
    }
</script>
