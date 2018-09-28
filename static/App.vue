<template>
    <div class="full-width containert">
        <h1>Optimus</h1>

        <div class="container">
            <div class="left-column">
                <file-upload @file_uploaded="onFileUploaded"></file-upload>
            </div>
            <div class="mid-column">
                <schema-editor :source="source" @schema_generated="onSchemaGenerated"></schema-editor>
            </div>
            <div class="right-column">
                <transformer :source="source" :schema="schema"></transformer>
            </div>
        </div>
    </div>

</template>

<script>
    import HeaderComponent from './components/Header.vue'
    import FileUpload from './components/FileUpload.vue'
    import SchemaEditor from './components/SchemaEditor.vue'
    import Transformer from './components/Transformer.vue'

    const data = {
        source: null,
        schema: null,
        transformed: null,
    }

    export default {
        components: {
            HeaderComponent,
            FileUpload,
            SchemaEditor,
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
