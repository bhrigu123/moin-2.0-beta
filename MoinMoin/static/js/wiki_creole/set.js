// ----------------------------------------------------------------------------
// markItUp!
// ----------------------------------------------------------------------------
// Copyright (C) 2008 Jay Salvat
// http://markitup.jaysalvat.com/
// ----------------------------------------------------------------------------
myMarkdownSettings = {
    nameSpace:          'markdown', // Useful to prevent multi-instances CSS conflict
    previewParserPath:  '~/sets/markdown/preview.php',
    onShiftEnter:       {keepDefault:false, openWith:'\n\n'},
    markupSet: [
        {name:'First Level Heading', key:"1",openWith:'== ',closeWith:' =', placeHolder:'Your title here...' } ,
        {name:'Second Level Heading', key:"2",openWith:'== ',closeWith:' ==', placeHolder:'Your title here...' },
        {name:'Heading 3', key:"3", openWith:'=== ',closeWith:' ===', placeHolder:'Your title here...' },
        {name:'Heading 4', key:"4", openWith:'==== ',closeWith:' ====', placeHolder:'Your title here...' },
        {name:'Heading 5', key:"5", openWith:'===== ',closeWith:' =====', placeHolder:'Your title here...' },
        {name:'Heading 6', key:"6", openWith:'====== ',closeWith:' ======', placeHolder:'Your title here...' },
        {separator:'---------------' },
        {name:'Bold', key:"B", openWith:"**", closeWith:"**"},
        {name:'Italic', key:"I", openWith:"//", closeWith:"//"},
        {separator:'---------------' },
        {name:'Bulleted List', openWith:'* ' },
        {name:'Numeric List', openWith:'# '  },
        {separator:'---------------' },
        {name:'Picture', key:"P", replaceWith:' {{[![Url:!:http://]!]|[![Alternative text]!]}} '},
        {name:'Link', key:"L", replaceWith:' [[[![Url:!:http://]!] | [![Title]!] ]] ', placeHolder:'Your text to link here...' },
        {separator:'---------------'},
        {name:'Quotes', openWith:' '},
        {name:'Code Block / Code', openWith:'{{{ ', closeWith:' }}}'},
        {separator:'---------------'},
        {name:'Preview', call:'preview', className:"preview"}
    ]
}

// mIu nameSpace to avoid conflict.
miu = {
    markdownTitle: function(markItUp, char) {
        heading = '';
        n = $.trim(markItUp.selection||markItUp.placeHolder).length;
        for(i = 0; i < n; i++) {
            heading += char;
        }
        return '\n'+heading+'\n';
    }
}