module.exports=[93695,(a,b,c)=>{b.exports=a.x("next/dist/shared/lib/no-fallback-error.external.js",()=>require("next/dist/shared/lib/no-fallback-error.external.js"))},70864,a=>{a.n(a.i(33290))},2894,a=>{a.n(a.i(66188))},13718,a=>{a.n(a.i(85523))},18198,a=>{a.n(a.i(45518))},62212,a=>{a.n(a.i(66114))},60978,a=>{"use strict";var b=a.i(7997);function c(){return(0,b.jsx)("div",{className:"min-h-screen bg-gradient-to-b from-gray-900 via-gray-800 to-gray-900 text-white py-24",children:(0,b.jsxs)("div",{className:"container mx-auto px-4 max-w-2xl",children:[(0,b.jsx)("h1",{className:"text-4xl font-bold mb-4 text-center bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent",children:"Contact Us"}),(0,b.jsx)("p",{className:"text-gray-400 text-center mb-12",children:"Have questions? We'd love to hear from you."}),(0,b.jsx)("div",{className:"bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-2xl p-8",children:(0,b.jsxs)("form",{id:"contactForm",className:"space-y-6",children:[(0,b.jsxs)("div",{children:[(0,b.jsx)("label",{htmlFor:"name",className:"block text-sm font-medium text-gray-300 mb-2",children:"Name"}),(0,b.jsx)("input",{type:"text",id:"name",name:"name",required:!0,className:"w-full px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-lg focus:outline-none focus:border-blue-500 transition-colors",placeholder:"Your name"})]}),(0,b.jsxs)("div",{children:[(0,b.jsx)("label",{htmlFor:"email",className:"block text-sm font-medium text-gray-300 mb-2",children:"Email"}),(0,b.jsx)("input",{type:"email",id:"email",name:"email",required:!0,className:"w-full px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-lg focus:outline-none focus:border-blue-500 transition-colors",placeholder:"your@email.com"})]}),(0,b.jsxs)("div",{children:[(0,b.jsx)("label",{htmlFor:"message",className:"block text-sm font-medium text-gray-300 mb-2",children:"Message"}),(0,b.jsx)("textarea",{id:"message",name:"message",required:!0,rows:6,className:"w-full px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-lg focus:outline-none focus:border-blue-500 transition-colors resize-none",placeholder:"How can we help you?"})]}),(0,b.jsx)("div",{id:"formStatus",className:"hidden text-center py-2 rounded-lg"}),(0,b.jsx)("button",{type:"submit",className:"w-full py-3 px-6 bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 rounded-lg font-semibold transition-all duration-200 transform hover:scale-[1.02]",children:"Send Message"})]})}),(0,b.jsx)("script",{dangerouslySetInnerHTML:{__html:`
          document.getElementById('contactForm')?.addEventListener('submit', async (e) => {
            e.preventDefault();
            const form = e.target;
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            const status = document.getElementById('formStatus');
            const button = form.querySelector('button[type="submit"]');

            button.disabled = true;
            button.textContent = 'Sending...';

            try {
              const response = await fetch('/api/contact', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
              });

              const result = await response.json();

              if (response.ok) {
                status.className = 'block text-center py-2 rounded-lg bg-green-500/20 text-green-400 border border-green-500/50';
                status.textContent = result.message || 'Message sent successfully!';
                form.reset();
              } else {
                throw new Error(result.error || 'Failed to send message');
              }
            } catch (error) {
              status.className = 'block text-center py-2 rounded-lg bg-red-500/20 text-red-400 border border-red-500/50';
              status.textContent = error.message || 'Something went wrong. Please try again.';
            } finally {
              button.disabled = false;
              button.textContent = 'Send Message';
            }
          });
        `}})]})})}a.s(["default",()=>c,"metadata",0,{title:"Contact Us | EchoPilotAI",description:"Get in touch with EchoPilotAI support team"}])}];

//# sourceMappingURL=%5Broot-of-the-server%5D__deabe5ee._.js.map