const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const dislikeSchema = mongoose.Schema({
    userId: {
        type:Schema.Types.ObjectId,
        ref: 'User'
    },
    commentId: {
        type:Schema.Types.ObjectId,
        ref: 'Comment'
    },
    postId: {
        type:Schema.Types.ObjectId,
        ref: 'Board'
    }

}, { timestamps: true })
  
    
const Dislike = mongoose.model('Dislike', dislikeSchema);

module.exports = { Dislike }