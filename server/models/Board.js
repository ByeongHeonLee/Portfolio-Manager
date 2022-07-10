const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const boardSchema = mongoose.Schema({
    writer: {
        type:Schema.Types.ObjectId,
        ref: 'User'
    },
    title: {
        type:String,
        maxlength:50,
    },
    description: {
        type: String,
    },
    // privacy: { 비밀글용도
    //     type: Number,
    // },
    filePath : {
        type: String,
    },
    views : {
        type: Number,
        default: 0 
    }
}, { timestamps: true })
  
    
const Board = mongoose.model('Board', boardSchema);

module.exports = { Board }