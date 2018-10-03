<template>
    <div class="full-width">
        <h1><a href="/"><> <> <></a></h1>

        <div class="container">
            <div class="column">
                <file-upload @file_uploaded="onFileUploaded"></file-upload>
            </div>
            <div class="column">
                <schema-editor :source="source" @schema_generated="onSchemaGenerated"></schema-editor>
            </div>
            <div class="column">
                <schema-renderer :schema="schema" v-on:update:schema="onSchemaGenerated"></schema-renderer>
            </div>
            <div class="column">
                <transformer :source="source" :schema="schema"></transformer>
            </div>
        </div>
    </div>

</template>

<script>
    import HeaderComponent from './components/Header.vue'
    import FileUpload from './components/FileUpload.vue'
    import SchemaEditor from './components/SchemaEditor.vue'
    import SchemaRenderer from './components/schema_renderer/SchemaRenderer.vue'
    import Transformer from './components/Transformer.vue'

    const data = {
        source: null,
        schema: null,
        name: null,
        transformed: null,
    }

    export default {
        components: {
            HeaderComponent,
            FileUpload,
            SchemaEditor,
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
